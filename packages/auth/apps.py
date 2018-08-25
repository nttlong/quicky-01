from . import models
import qmongo
def create_app(name):
    app = models.entities.apps.mk_obj()
    app.name = name
    ret=  models.entities.apps.insert_one(app)
    return ret.data,ret.error
def get_app(name):
    ret_data = models.entities.apps.coll.aggregate().match("name=={0}",name).get_item()
    if ret_data == None:
        return None
    return qmongo.create(ret_data)
def add_schema_to_app(name,schema):
    app = get_app(name)
    if app == None:
        return None, dict(message="'{0}' was not found".format(name),code="not_found")
    with qmongo.set_except_mode("return"):
        qr= models.entities.apps.coll
        qr = qr.aggregate()
        qr = qr.match("name=={0}", name)





