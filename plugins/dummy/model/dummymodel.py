from collectionsamplemodel import CollectionSampleModel
from collectionsamplemodel import CollectionResourceSampleModel
from progresssamplemodel import ProgressSampleModel
from resourcesamplemodel import ResourceSampleModel

from backend import config
from backend.basemodel import BaseModel
from backend.objectstore import ObjectStore


class DummyModel(BaseModel):
    def __init__(self):
        objstore_loc = config.get_object_store()
        self.objstore = ObjectStore(objstore_loc)

        sub_models = []
        collectionsample = CollectionSampleModel()
        collectionresourcesample = \
            CollectionResourceSampleModel(collectionsample)
        resourcesample = ResourceSampleModel()
        progresssample = ProgressSampleModel(objstore=self.objstore)

        sub_models = [
            collectionresourcesample,
            collectionsample,
            progresssample,
            resourcesample]
        return super(DummyModel, self).__init__(sub_models)
