from backend.control.base import Resource


class ProgressSample(Resource):
    def __init__(self, model, ident=None):
        super(ProgressSample, self).__init__(model, ident)
        self.uri_fmt = "/progresssample/%s"
        self.progress = self.generate_action_handler_task('progress')

    @property
    def data(self):
        return self.info
