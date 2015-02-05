from kimchi.exception import InvalidOperation, NotFoundError


class CollectionSampleModel(object):
    def __init__(self):
        self._resources = {}

    def create(self, params):
        nic = params['nic']
        if nic in self._resources:
            raise InvalidOperation("SPRET0001E", {'nic': nic})
        self._resources[nic] = ResourceElementSample(params['onboot'], params['bootproto'])
        return nic

    def get_list(self):
        return sorted(self._resources)


class CollectionResourceSampleModel(object):
    def __init__(self, parent_model):
        self._resources = parent_model._resources

    def lookup(self, nic):
        try:
            resource = self._resources[nic]
        except KeyError:
            raise NotFoundError("SPRET0002E", {'nic': nic})
        return {'onboot': resource.onboot, 'bootproto': resource.bootproto}

    def update(self, nic, params):
        if nic not in self._resources:
            raise NotFoundError("SPRET0002E", {'nic': nic})
        try:
            self._resources[nic].onboot = params['onboot']
        except KeyError:
            pass

        try:
            self._resources[nic].bootproto = params['bootproto']
        except KeyError:
            pass
        return nic

    def delete(self, nic):
        try:
            del self._resources[nic]
        except KeyError:
            pass


class ResourceElementSample(object):
    def __init__(self, onboot, bootproto):
        self.onboot = onboot
        self.bootproto = bootproto
