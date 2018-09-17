import qmongo
from qmongo import connection
class __models__(object):
    def __init__(self,schema):
        self.__schema__ =schema
    @property
    def connection(self):
        from django.conf import settings
        from qmongo import database
        st =settings.DATABASES['default']
        return database.connect(
            host=st["HOST"],
            port=st["PORT"],
            name=st["NAME"],
            user=st["USER"],
            password=st["PASSWORD"]).db

    @property
    def apps(self):
        from django.conf import settings
        from . import models
        ret = models.entities.apps.coll.set_schema(self.__schema__)
        ret.qr.db = self.connection
        return ret
    @property
    def entities(self):
        from . import models
        return models.entities
class auth(object):
    def __init__(self):
        self.__schema__ ='sys'
        self.__models__ = __models__(self.__schema__)
    @property
    def models(self):
        return self.__models__
    def get_app(self,name):
        ret = self.models.apps.where("name==@app_name",app_name=name).object
        return ret
    def create_app(self, name):
        """
        Create app
        :param name:
        :return:
        """
        with qmongo.except_mode("return"):
            app =  self.models.entities.apps.mk_obj()
            app.name = name
            ret = self.models.apps.insert_one(app)
            return app,ret[1],ret[2]
    def app_add_schema(self,name,schema):
        app =self.get_app(name)
        if app == None:
            message = "App '{0}' was not found".format(name)
            return None,qmongo.fx_model.s_obj(message=message),message
        elif app.schemas.count(schema)>0:
            return app,None,"Schema '{0}' is existing in app '{a}'"
        else:
            with qmongo.except_mode("return"):
                ret,ex,msg = self.models.apps.where("name=={0} and schemas!={1}",name,schema).push(schemas=schema).commit()
                if ex!=None:
                    return app,ex,msg
                else:
                    app = self.get_app(name)
                    return app,None,"Add schema '{0}' to app '{1}' is successful ".format(schema,name)
    def app_add_view(self,name,viewpath):
        app = self.get_app(name)
        if app == None:
            message = "App '{0}' was not found".format(name)
            return None, qmongo.fx_model.s_obj(message=message), message
        else:
            _find_views_ = [x for x in app.views if x.path==viewpath]
            if _find_views_.__len__()>0:
                return app, None, "View '{0}' is existing in app '{1}' is successful ".format(viewpath, name)

            with qmongo.except_mode("return"):
                ret, ex, msg = self.models.apps.where("name=={0} and views.path!={1}", name,viewpath).push(views=dict(
                    path=viewpath,
                    name=viewpath,
                    is_public=False,
                    privileges=[],
                    roles=[]
                )).commit()
                if ex != None:
                    return app, ex, msg
                else:
                    app = self.get_app(name)
                    return app, None, "Add view '{0}' to app '{1}' is successful ".format(viewpath, name)



global authorize
authorize = auth()