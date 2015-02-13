from backend.control.base import Resource, Collection


class CollectionSample(Collection):
    def __init__(self, model):
        super(CollectionSample, self).__init__(model)
        self.resource = CollectionResourceSample


class CollectionResourceSample(Resource):
    def __init__(self, model, ident):
        super(CollectionResourceSample, self).__init__(model, ident)
        self.update_params = ['onboot', 'bootproto']

    @property
    def data(self):
        self.info.update({'nic': self.ident})
        return self.info
