from backend.model.tasks import TaskModel
from backend.utils import add_task
from time import sleep


class ProgressSampleModel(object):
    def __init__(self, **kargs):
        self.objstore = kargs['objstore']
        self.task = TaskModel(**kargs)

    def progress(self, *name):
        progress = DummyProgress()

        taskid = add_task('/progresssample/progress', progress.doProgress,
                          self.objstore, None)
        return self.task.lookup(taskid)


class DummyProgress(object):
    def __init__(self):
        self.text = 'Step'

    def doProgress(self, cb, params):
        # reset messages
        cb('')
        for i in range(2):
            cb("%s %s" % (self.text, i))
            sleep(10)
        return cb("Done", True)
