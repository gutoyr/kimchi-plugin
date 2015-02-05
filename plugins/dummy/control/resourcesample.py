from kimchi.control.base import Resource


class ResourceSample(Resource):
    def __init__(self, model, ident=None):
        super(ResourceSample, self).__init__(model, ident)
        self.update_params = ['state']
        self.uri_fmt = "/resourcesample/%s"
        self.start = self.generate_action_handler('start')

    @property
    def data(self):
        return self.info
