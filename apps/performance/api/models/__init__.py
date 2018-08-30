import django
import quicky
import authorization
import qmongo

from qmongo import database, helpers
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)
def load_all_functions():
    import imp
    import sys
    from types import ModuleType
    import lv.models
    mdl = sys.modules[__name__]

    x = [ k for k,v in lv.models.entities.__dict__.items()]
    modules = [(k,getattr(lv.models, k)) for k in x if isinstance(getattr(lv.models, k), ModuleType)]
    for name,_module_ in modules:
        setattr(mdl,name,_module_)
        _x = imp.new_module(__name__+"."+name)
        setattr(_x,name,getattr(_module_,name))


load_all_functions()




from ..views import *
import pymongo
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

def create_session():
    session = db_context.db.client.start_session()
    return session
def start_transaction(session):
    session.start_transaction(
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority"))
    return session

def abort_transaction(session):
    session.abort_transaction()
    return  session

def end_session(session):
    session.end_session()

def commit_transaction(session):
    session.commit_transaction()