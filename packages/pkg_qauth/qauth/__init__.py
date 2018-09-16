VERSION = [1,0,0,"final",0]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
from pymongo import mongo_client
from sqlalchemy.sql import quoted_name

from . import models
import qmongo
from qobjects import lazyobject
from . import exceptions
global __schema__
__schema__ = "sys"
from . import  authorize
auth = authorize.authorize
def schema(_schema):
    __schema__ = _schema
def create_app(name):
    """
    Create app
    :param name:
    :return:
    """
    with qmongo.except_mode("return"):
        app = models.entities.apps.mk_obj()
        app.name = name
        ret =  models.entities.apps.coll.set_schema(__schema__).insert_one(app)
        return ret
def remove_app(name):
    with qmongo.except_mode("return"):
        ret = models.entities.apps.coll.set_schema(__schema__).delete("name=={0}", name)
        return ret
def app_get(name):
    ret_data = models.entities.apps.coll.set_schema(__schema__).aggregate().match("name=={0}",name).get_item()
    if ret_data == None:
        return None
    return qmongo.create(ret_data)
def app_add_schema(name,schema):
    app = app_get(name)
    if app == None:
        return None, \
               lazyobject(
                   message="'{0}' was not found".format(name),
                   code="not_found"
               ),\
               "'{0}' was not found".format(name)
    with qmongo.except_mode("return"):
        qr= models.entities.apps.coll.set_schema(__schema__)
        qr = qr.aggregate()
        qr = qr.match("name=={0}", name)
        qr.project([schema], index_of_schema="indexOfArray(schemas,{0})")
        result= qr.get_object()
        if result.index_of_schema == None or result.index_of_schema == -1:
            ret,ex =models.entities.apps.coll.set_schema(__schema__).where("name=={0}", name).push(schemas=schema).commit()
            return None,ex,None
        else:
            return None, None, "'{0}/{1}' is already existing".format(name,schema)
    return None,None,None
def app_remove_schema(name,schema):
    app = app_get(name)
    if app == None:
        return None, \
                   lazyobject(
                       message="'{0}' was not found".format(name),
                       code="not_found"
                       ),"'{0}' was not found".format(name)
    with qmongo.except_mode("return"):
        qr = models.entities.apps.coll.set_schema(__schema__)
        qr = qr.aggregate()
        qr = qr.match("name=={0}", name)
        qr.project([schema], index_of_schema="indexOfArray(schemas,{0})")
        result = qr.get_object()
        if result.index_of_schema == None or result.index_of_schema == -1:
            return None, None,"Schema '{0}' was not found in '{1}'".format(schema,name)
        else:
            ret , ex =models.entities.apps.coll.where("name=={0}", name).pull(schemas=schema).commit()
            return ret,ex,None
def app_add_view(name,path,view=None,is_public=False,privileges=[]):
    if view == None:
        view = path
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(message="'{0}' was not found".format(name), code="not_found"),\
               "'{0}' was not found".format(name)

    with qmongo.except_mode("return"):
        qr = models.entities.apps.coll.set_schema(__schema__).aggregate()
        qr = qr.match("name=={0}", name)
        qr = qr.project([path], index_of_view="indexOfArray(views.path,{0})")
        result = qr.get_object()
        if result.index_of_view == None or result.index_of_view == -1:
            actor = models.entities.apps.coll.set_schema(__schema__).where("name=={0}", name)
            actor.push(views=dict(
                name=view,
                path = path,
                is_public= is_public,
                privileges= privileges
            ))
            ret,ex = actor.commit()
            return None,ex,"Insert new view {0} with path={1} in {2}".format(view,path,name)
        else:
            actor = models.entities.apps.coll.set_schema(__schema__).where("name=={0}",name)
            actor =actor.set({
                "views.{0}".format(result.index_of_view):dict(
                    name=view,
                    path=path,
                    is_public=is_public,
                    privileges=privileges
                )
            })
            ret ,ex = actor.commit()
            return None,ex, "Update new view {0} with path={1} in {2}".format(view,path,name)
def app_remove_view(name,path):
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(message="'{0}' was not found".format(name), code="not_found"),\
               "'{0}' was not found".format(name)

    with qmongo.except_mode("return"):
        qr = models.entities.apps.coll.set_schema(__schema__).aggregate()
        qr = qr.match("name=={0}", name)
        qr = qr.project([path], index_of_view="indexOfArray(views.path,{0})")
        result = qr.get_object()
        if result.index_of_view == None or result.index_of_view == -1:
            return None,None,"View with path={0} is not in {1}".format(path,name)
        else:
            actor = models.entities.apps.coll.where("name=={0}",name)
            actor =actor.pull({"views":{"path":path}})
            ret ,ex = actor.commit()
            return None,ex, "'{0}' has remove  view with path={1}".format(name,path)
def role_get(role):
    return models.entities.roles.coll.set_schema(__schema__).aggregate().match("role=={0}",role).get_object()
def role_create(role,name,description = None,users =[]):
    """
    Create role
    :param role: role code
    :param name: role name
    :param description: description of role
    :param users: list of username are in role
    :return: role
    """
    role_item = role_get(role)
    if role_item != None:
        return None,\
               lazyobject(
                   code="not_found",
                   message="Role '{0}' was not found"
               ),\
               "'{0}' is already existing"
    with qmongo.except_mode('return'):
        entity = models.entities.roles.coll.set_schema(__schema__)
        ret, ex =  entity.insert_one(role=role,name = name,description=description,user=users)
        if ex != None:
            return None,ex,"Create role '{0}' is error".format(role)
        else:
            role_item = role_get(name)
            return role_item, None, "Create role '{0}' is successfull".format(role)
def app_modify_role(name,view_path,role,is_full_access = False,privileges =[]):
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(
                   message = "App '{0}' was not found".format(name),
                   code="not_found"
               ),\
               "'{0}' was not found".format(name)
    role_item =role_get(role)
    if role_item == None:
        return None, \
               lazyobject(
                   message="Role '{0}' was not found".format(name),
                   code="not_found"
               ), \
               "'{0}' was not found".format(name)
    qr = models.entities.apps.coll.set_schema(__schema__).aggregate()
    qr= qr.match("name=={0}",name)
    qr=qr.project(
        [view_path],
        index_of_view = "indexOfArray(views.path,{0})",
        views =1
    )
    qr=qr.unwind("views")
    qr=qr.match("views.path=={0}",view_path)
    qr=qr.project(
        [role],
        index_of_view =1,
        index_of_role="indexOfArray(views.roles.role,{0})",
        views=1
    )
    result = qr.get_object()
    if result == None:
        return None, \
               lazyobject(
                   message="View '{0}' was not found".format(view_path),
                   code="not_found"
               ), "View '{0}' was not found".format(view_path)
    if result.index_of_view == None or result.index_of_view == -1:
        return None,\
               lazyobject(
                   message="View '{0}' was not found".format(view_path),
                   code="not_found"
               ),"View '{0}' was not found".format(view_path)
    set_of_input_privilegs =set(privileges)
    set_of_privileges_in_view =set(result.views.privileges)
    result_set = set_of_input_privilegs.difference(set_of_privileges_in_view)
    if result_set.__len__()>0:
        return None,lazyobject(
            code="invalid_data",
            message = "Error: Value {0} is not in {1}".format(list(result_set),list(set_of_privileges_in_view))
        ),"Error: Value {0} is not in {1}".format(list(result_set),list(set_of_privileges_in_view))
    _privileges = list(set(result.views.privileges).intersection(privileges))
    if result.index_of_role == None or result.index_of_role == -1:
        with qmongo.except_mode("return"):
            entity = models.entities.apps.coll.set_schema(__schema__)
            actor=entity.where("name=={0}", name)
            actor=actor.push({"views.{0}.roles".format(result.index_of_view): dict(
                role=role,
                is_full_access=is_full_access,
                privileges=privileges
            )})
            ret,ex =actor.commit()
            if ex!=None:
                return None,\
                       lazyobject(ex),\
                       "Add role '{0}' to view '{1}' of app '{2}' is error".format(role,view_path,name)
            else:
                return None, \
                       None, \
                       "Add role '{0}' to view '{1}' of app '{2}' is successfull".format(role, view_path, name)
    else:
        with qmongo.except_mode("return"):
            entity = models.entities.apps.coll.set_schema(__schema__)
            actor = entity.where("name=={0}", name)
            actor = actor.set({
                "views.{0}.roles.{1}".format(result.index_of_view,result.index_of_role):
                    dict(
                        role=role,
                        is_full_access=is_full_access,
                        privileges=privileges
                    )
            })
            ret, ex = actor.commit()
            if ex != None:
                return None, \
                       lazyobject(ex), \
                       "Update role '{0}' to view '{1}' of app '{2}' is error".format(role, view_path, name)
            else:
                return None, \
                       None, \
                       "Update role '{0}' to view '{1}' of app '{2}' is successfull".format(role, view_path, name)
def app_remove_role(name,view_path,role):
    app = app_get(name)
    if app == None:
        return None, \
               lazyobject(
                   message="App '{0}' was not found".format(name),
                   code="not_found"
               ), \
               "'{0}' was not found".format(name)
    role_item = role_get(role)
    if role_item == None:
        return None, \
               lazyobject(
                   message="Role '{0}' was not found".format(name),
                   code="not_found"
               ), \
               "'{0}' was not found".format(name)
    qr = models.entities.apps.coll.set_schema(__schema__).aggregate()
    qr = qr.match("name=={0}", name)
    qr = qr.project(
        [view_path],
        index_of_view="indexOfArray(views.path,{0})",
        views=1
    )
    qr = qr.unwind("views")
    qr = qr.match("views.path=={0}", view_path)
    qr = qr.project(
        [role],
        index_of_view=1,
        index_of_role="indexOfArray(views.roles.role,{0})",
        views=1
    )
    result = qr.get_object()
    if result == None:
        return None, \
               lazyobject(
                   message="View '{0}' was not found".format(view_path),
                   code="not_found"
               ), "View '{0}' was not found".format(view_path)
    if result.index_of_view == None or result.index_of_view == -1:
        return None, \
               lazyobject(
                   message="View '{0}' was not found".format(view_path),
                   code="not_found"
               ), "View '{0}' was not found".format(view_path)
    if result.index_of_role == None or result.index_of_role == -1:
        return None,None,"Role '{0}' was not found in view '{1}' of app '{2}'".format(role,view_path,name)
    else:
        with qmongo.except_mode("return"):
            entity = models.entities.apps.coll.set_schema(__schema__)
            actor = entity.where("name=={0}", name)
            actor = actor.pull({"views.{0}.roles".format(result.index_of_view):
                                    dict(
                                        role=role
                                    )
                                })
            ret, ex = actor.commit()
            if ex != None:
                return None, \
                       lazyobject(ex), \
                       "Remove role '{0}' to view '{1}' of app '{2}' is error".format(role, view_path, name)
            else:
                return None, \
                       None, \
                       "Remove role '{0}' to view '{1}' of app '{2}' is successfull".format(role, view_path, name)
def role_add_user(role,username):
    role_item =role_get(role)
    if role_item == None:
        return None,lazyobject(
            code="not_found",
            message = "role '{0}' was not found".format(role)
        ),"role '{0}' was not found".format(role)
    entity = models.entities.roles.coll.set_schema(__schema__)
    qr = models.entities.roles.coll.aggregate()
    qr= qr.match("role=={0}",role)
    qr =qr.project([username],index_of_user="indexOfArray(users,{0})")
    result =qr.get_object()
    if result == None or result.index_of_user==None or result.index_of_user ==-1:
        with qmongo.except_mode("return"):
            actor=entity.where("role == {0}",role)
            actor=actor.push(users=username)
            ret,ex =actor.commit()
            return None,lazyobject(ex),"Add user to role '{0}' is successfull".format(role)
def get_list_of_apps_of_user(username,schema):
    apps = models.entities.apps.coll.set_schema(__schema__)
    roles = models.entities.roles.coll.set_schema(__schema__)
    qr = apps.aggregate().match("schemas=={0}",schema)
    qr.unwind("views")
    qr.lookup(roles, "views.roles.role", "role", "roles")
    qr.match("roles.users=={0}", username)
    qr.project(
        name=1,
        schemas=1,
        views=1)
    return list(qr.get_objects())







