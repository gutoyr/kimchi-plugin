#
# Project Kimchi
#
# Copyright IBM, Corp. 2013-2014
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

import json
import os
import unittest


from functools import partial


import kimchi.mockmodel
import kimchi.server
from kimchi.utils import get_enabled_plugins
from utils import get_free_port, patch_auth, request
from utils import run_server
import time
from kimchi import config


test_server = None
model = None
host = None
port = None
ssl_port = None
objstore_loc = None


def setUpModule():
    global test_server, model, host, port, ssl_port, objstore_loc

    patch_auth()
    objstore_loc = config.get_object_store()
    model = kimchi.mockmodel.MockModel(objstore_loc)
    host = '127.0.0.1'
    port = get_free_port('http')
    ssl_port = get_free_port('https')
    test_server = run_server(host, port, ssl_port, test_mode=True,
                             model=model)


def tearDownModule():
    test_server.stop()
    os.unlink(objstore_loc)


@unittest.skipUnless(
    'dummy' in [plugin for plugin, _config in get_enabled_plugins()],
    'dummy plugin is not enabled, skip this test!')
class PluginTests(unittest.TestCase):

    def setUp(self):
        self.request = partial(request, host, ssl_port)

    # Colletcion/Resource Sample
    def _create_resource(self, nic, onboot, bootproto):
        req = json.dumps({'nic': nic, 'onboot': onboot, 'bootproto': bootproto})
        resp = self.request('/plugins/dummy/collectionsample', req, 'POST')
        return resp

    def _get_resource(self, nic):
        resp = self.request('/plugins/dummy/collectionsample/%s' % nic)
        return json.loads(resp.read())

    def _create_resource_and_assert(self, nic, onboot, bootproto):
        resp = self._create_resource(nic, onboot, bootproto)
        self.assertEquals(201, resp.status)

        resource = self._get_resource(nic)
        self.assertEquals(resource['nic'], nic)
        self.assertEquals(resource['onboot'], onboot)
        self.assertEquals(resource['bootproto'], bootproto)

    def _get_collectionsample_list(self):
        resp = self.request('/plugins/dummy/collectionsample')
        collection = json.loads(resp.read())
        nic_list = [resource['nic'] for resource in collection]
        return nic_list

    def test_collectionsample(self):
        # Colection + resource
        # Create two new resources
        self._create_resource_and_assert('eth0', 9, 99)
        self._create_resource_and_assert('eth1', 1, 11)

        # Verify they're in the list
        nic_list = self._get_collectionsample_list()
        self.assertIn('eth0', nic_list)
        self.assertIn('eth1', nic_list)

        # Update the eth1 resource.
        req = json.dumps({'onboot': 2, 'bootproto': 22})
        resp = self.request('/plugins/dummy/collectionsample/eth1', req, 'PUT')
        self.assertEquals(200, resp.status)
        eth1 = self._get_resource('eth1')
        self.assertEquals(eth1['onboot'], 2)
        self.assertEquals(eth1['bootproto'], 22)

        # Delete two resources from collection
        resp = self.request('/plugins/dummy/collectionsample/eth1', '{}', 'DELETE')
        self.assertEquals(204, resp.status)
        resp = self.request('/plugins/dummy/collectionsample/eth0', '{}', 'DELETE')
        self.assertEquals(204, resp.status)
        nic_list = self._get_collectionsample_list()
        self.assertEquals([], nic_list)

    # Resource Sample
    def _get_status(self):
        resp = self.request('/plugins/dummy/resourcesample')
        return json.loads(resp.read())

    def test_resourcesample(self):
        # Resource
        # Create state
        resp = self.request('/plugins/dummy/resourcesample/start', '{}', 'POST')
        self.assertEquals(200, resp.status)
        status = self._get_status()
        self.assertEquals(status['state'], 'Step00')

        # Update state
        state = 'Step01'
        req = json.dumps({'state': state})
        resp = self.request('/plugins/dummy/resourcesample', req, 'PUT')
        self.assertEquals(200, resp.status)
        status = self._get_status()
        self.assertEquals(status['state'], state)

        # Delete state
        resp = self.request('/plugins/dummy/resourcesample', '{}', 'DELETE')
        self.assertEquals(204, resp.status)
        status = self._get_status()
        self.assertEquals(status['state'], None)

    # Progress Sample
    def test_progresssample(self):
        resp = self.request('/plugins/dummy/progresssample/progress', {}, 'POST')
        task = json.loads(resp.read())
        task_params = [u'id', u'message', u'status', u'target_uri']
        self.assertEquals(sorted(task_params), sorted(task.keys()))

        resp = self.request('/tasks/' + task[u'id'], None, 'GET')
        task_info = json.loads(resp.read())
        self.assertEquals(sorted(task_params), sorted(task_info.keys()))
        self.assertEquals(task_info['status'], 'running')
        self.assertIn(u'Step 0', task_info['message'])
        time.sleep(5)
        resp = self.request('/tasks/' + task[u'id'], None, 'GET')
        task_info = json.loads(resp.read())
        self.assertEquals(task_info['status'], 'running')
        self.assertIn(u'Step 1', task_info['message'])
        time.sleep(5)
        resp = self.request('/tasks/' + task[u'id'], None, 'GET')
        task_info = json.loads(resp.read())
        self.assertEquals(task_info['status'], 'finished')
        self.assertIn(u'Done', task_info['message'])

    def test_bad_params(self):
        # Bad nic
        resp = self._create_resource(1.0, 30, 40)
        self.assertEquals(400, resp.status)

        # Bad onboot value
        resp = self._create_resource('test', -10.0, 40)
        self.assertEquals(400, resp.status)

        # Bad bootproto value
        resp = self._create_resource('test', 9, 0)
        self.assertEquals(400, resp.status)

        # Missing param for bootproto
        req = json.dumps({'nic': 'nobootproto', 'onboot': 40})
        resp = self.request('/plugins/dummy/collectionsample', req, 'POST')
        self.assertEquals(400, resp.status)
