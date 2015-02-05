import json
import os


from cherrypy import expose


from kimchi.config import PluginPaths
from kimchi.root import Root
from plugins.dummy.i18n import messages
from plugins.dummy.model import DummyModel
from plugins.dummy.control import ProgressSample
from plugins.dummy.control import CollectionSample
from plugins.dummy.control import ResourceSample


class Dummy(Root):
    def __init__(self):
        self.model = DummyModel()
        super(Dummy, self).__init__(self.model)
        self.collectionsample = CollectionSample(self.model)
        self.resourcesample = ResourceSample(self.model)
        self.progresssample = ProgressSample(self.model)
        self.paths = PluginPaths('dummy')
        self.domain = 'dummy'
        self.messages = messages
        self.api_schema = json.load(open(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'API.json')))

    @expose
    def index(self):
        return 'This is dummy plugin for Kimchi'
