class listofviews(dict):
    def __setitem__(self, item, value):
        print "You are changing the value of %s to %s!!"%(item, value)
        super(listofviews, self).__setitem__(item, value)
    def __getitem__(self, item):

        ret = super(listofviews, self).__getitem__(item)
        schema = ret.get_collection_name().split('.')[0]
        def __create_as_view__(schema):
            ret.__create_mongodb_view__(ret,"{0}.{1}".format(schema,ret.__source_name__))
        setattr(ret, "__create_as_view__", __create_as_view__)
        return ret
global _cach_view
_cach_view=listofviews()
global __cach_has_exec_command_create_view__
__cach_has_exec_command_create_view__ = {}

from . database import AGGREGATE
from . import helpers
from . import fx_model
from . import models
class __views__(object):
    pass
def create_mongodb_view(aggregate,name):
    if not isinstance(aggregate,AGGREGATE):
        raise (Exception("It looks like you create view from object is not '{0}'".format("qmomgo.database.AGGREGATE")))
    global _cach_view
    def __create_mongodb_view__(self,sourcename):
        def excec_command():
            import json
            context = self.qr.db
            context = self.qr.db
            if context == None:
                from . import db_context
                context = db_context.get_db_context()
                if context == None:
                    raise (Exception("Please use:\n"
                                     "import qmongo\n"
                                     "qmongo.set_db_context(host=..,port=..,user=..,password=..,name=...)\n"
                                     "or you can use bellow statement:\n"
                                     "qmongo.set_db_context(\"mongodb://{username}:{password}@{host}:{port}/{database name}[:{schema}]\")"))
                else:
                    self.qr.db = context.db
            if self.schema == None or self.schema == "":
                from .db_context import get_schema
                self.schema = get_schema()
            view_name = self._none_schema_name
            if self.schema != None and self.schema !="":
                view_name = "{0}.{1}".format(self.schema, self._none_schema_name)

            command_object = (
                view_name,
                sourcename,
                self.__initial_pipe__
            )
            self.qr.db.drop_collection(view_name)
            param_text = json.dumps(command_object)
            param_text = param_text[1:param_text.__len__() - 1]
            command_text = "db.createView(" + param_text + ")"
            self.qr.db.eval(command_text)
        if not __cach_has_exec_command_create_view__.has_key("{0}.{1}".format(self.schema,self._none_schema_name)):
            excec_command()
    if not _cach_view.has_key(name):
        view_model_fields={}
        for field in aggregate.get_selected_fields():
            view_model_fields.update(
                {field:helpers.create_field("text", False)}
            )

        helpers.define_model(
            name,
            [],
            view_model_fields
        )
        if not hasattr(models,"views"):
            views = __views__()
            setattr(models,"views",views)
        else:
            views = getattr(models,"views")
        # view_define = getattr(models,name)
        # setattr(views,name,view_define)
        # delattr(models,name)
        ret=aggregate.qr.collection(name)
        if not hasattr(ret,"__create_mongodb_view__"):
            setattr(ret,"__create_mongodb_view__",__create_mongodb_view__)
            setattr(ret,"__source_name__",aggregate._coll._none_schema_name)
            setattr(ret, "__initial_pipe__", [x.copy() for x in aggregate._pipe])
        _cach_view[name] = ret
        import qmongo
        if not hasattr(qmongo,"views"):
            setattr(qmongo,"views",__views__())
        _views = getattr(qmongo,"views")
        if hasattr(qmongo.models, name):
            view_entity = getattr(qmongo.models, name)
            setattr(_views,name,view_entity)
            delattr(qmongo.models, name)


        return _cach_view[name]
    else:
        return _cach_view[name]
def create_mongod_view_from_pipeline(db,pipe_line,from_collection,schema,view_name):
    global _cach_view
    import json
    view_name = "{0}.views.{1}".format(schema, view_name)
    command_object = (
        view_name,
        "{0}.{1}".format(schema,from_collection),
        pipe_line
    )
    if not _cach_view.has_key(view_name):
        db.drop_collection(view_name)
        param_text = json.dumps(command_object)
        param_text = param_text[1:param_text.__len__() - 1]
        command_text = "db.createView(" + param_text + ")"
        db.eval(command_text)
        _cach_view[view_name] = 1
        view_model_fields={}
    return view_name
