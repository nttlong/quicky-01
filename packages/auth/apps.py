from . import models
import qmongo
def create_app(name):
    app = models.entities.apps.mk_obj()
    app.name = name
    ret=  models.entities.apps.insert_one(app)
    return ret.data,ret.error