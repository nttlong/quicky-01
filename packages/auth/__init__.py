from pymongo import mongo_client
from sqlalchemy.sql import quoted_name

from . import models
import qmongo
from qobjects import lazyobject
def create_app(name):
    """
    Create app
    :param name:
    :return:
    """
    with qmongo.exept_mode("return"):
        app = models.entities.apps.mk_obj()
        app.name = name
        ret=  models.entities.apps.insert_one(app)
        return ret
def app_get(name):
    ret_data = models.entities.apps.coll.aggregate().match("name=={0}",name).get_item()
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
    with qmongo.exept_mode("return"):
        qr= models.entities.apps.coll
        qr = qr.aggregate()
        qr = qr.match("name=={0}", name)
        qr.project([schema], index_of_schema="indexOfArray(schemas,{0})")
        result= qr.get_object()
        if result.index_of_schema == None or result.index_of_schema == -1:
            ret,ex,msg =models.entities.apps.coll.where("name=={0}", name).push(schemas=schema).commit()
            return None,ex,msg
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
    with qmongo.exept_mode("return"):
        qr = models.entities.apps.coll
        qr = qr.aggregate()
        qr = qr.match("name=={0}", name)
        qr.project([schema], index_of_schema="indexOfArray(schemas,{0})")
        result = qr.get_object()
        if result.index_of_schema == None or result.index_of_schema == -1:
            return None, None,"Schema '{0}' was not found in '{1}'".format(schema,name)
        else:
            ret , ex =models.entities.apps.coll.where("name=={0}", name).pull("schemas=={0}",schema).commit()
            return ret,ex,None
def app_add_view(name,path,view=None,is_public=False,privileges=[]):
    if view == None:
        view = path
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(message="'{0}' was not found".format(name), code="not_found"),\
               "'{0}' was not found".format(name)

    with qmongo.exept_mode("return"):
        qr = models.entities.apps.coll.aggregate()
        qr = qr.match("name=={0}", name)
        qr = qr.project([path], index_of_view="indexOfArray(views.path,{0})")
        result = qr.get_object()
        if result.index_of_view == None or result.index_of_view == -1:
            actor = models.entities.apps.coll.where("name=={0}", name)
            actor.push(views=dict(
                name=view,
                path = path,
                is_public= is_public,
                privileges= privileges
            ))
            ret,ex,msg = actor.commit()
            if ex == None:
                return ret,None,"Add view '{0}' to app '{1}' is successful".format(name,path)
            else:
                return None,ex,"Add view '{0}' to app '{1}' is error\n{2}".format(name,path,msg)
        else:
            actor = models.entities.apps.coll.where("name=={0}",name)
            actor =actor.set({
                "views.{0}".format(result.index_of_view):dict(
                    name=view,
                    path=path,
                    is_public=is_public,
                    privileges=privileges
                )
            })
            ret ,ex,msg = actor.commit()
            if ex == None:
                return ret,None,"Update view '{0}' of '{1}' is successful".format(path,name)
            else:
                return None,ex, "Update view '{0}' of '{1}' is error\n{2}".format(path,name,msg)
def app_remove_view(name,path):
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(message="'{0}' was not found".format(name), code="not_found"),\
               "'{0}' was not found".format(name)

    with qmongo.exept_mode("return"):
        qr = models.entities.apps.coll.aggregate()
        qr = qr.match("name=={0}", name)
        qr = qr.project([path], index_of_view="indexOfArray(views.path,{0})")
        result = qr.get_object()
        if result.index_of_view == None or result.index_of_view == -1:
            return None,None,"View with path={0} is not in {1}".format(path,name)
        else:
            actor = models.entities.apps.coll.where("name=={0}",name)
            actor =actor.pull("views.path=={0}",path)
            ret ,ex = actor.commit()
            return None,ex, "'{0}' has remove  view with path={1}".format(name,path)
def role_get(schema,role):
    return models.entities.roles.coll.aggregate().match("role=={0} and schema =={1}",role,schema).get_object()

def role_create(schema,role,name,description = None,users =[]):
    """
    Create role
    :param role: role code
    :param name: role name
    :param description: description of role
    :param users: list of username are in role
    :return: role
    """
    role_item = role_get(schema, role)
    if role_item != None:
        return None,\
               lazyobject(
                   code="not_found",
                   message="Role '{0}' in schema '{1}' is existing".format(role,schema)
               ),\
               "Role '{0}' in schema '{1}' is already existing".format(role,schema)
    schema_item = schema_get(schema)

    if schema_item == None:
        return None,\
               lazyobject(
                   code="not_found",
                   message="Schema '{0}' was not founsd ".format(schema)
               ),\
               "Schema '{0}' was not founsd ".format(schema)

    with qmongo.exept_mode('return'):
        entity = models.entities.roles.coll
        ret, ex,msg =  entity.insert_one(schema=schema, role=role,name = name,description=description,user=users)
        if ex != None:
            return None,ex,"Create role '{0}' is error,\n {1}".format(role,msg)
        else:
            role_item = role_get(schema, role)
            return role_item, None, "Create role '{0}' is successful".format(role)
def app_modify_role(name,view_path,schema,role,is_full_access = False,privileges =[]):
    app = app_get(name)
    if app == None:
        return None,\
               lazyobject(
                   message = "App '{0}' was not found".format(name),
                   code="not_found"
               ),\
               "'{0}' was not found".format(name)
    if app.schemas.count(schema) ==0 :
        return None,\
               lazyobject(
                   message="App '{0}' does not support schema '{1}".format(name,schema)),\
               "App '{0}' does not support schema '{1}".format(name,schema)

    role_item =role_get(schema,role)
    if role_item == None:
        return None, \
               lazyobject(
                   message="Role '{0}' was not found in schema '{1}'".format(role,schema),
                   code="not_found"
               ), \
               "Role '{0}' was not found in schema '{1}'".format(role,schema)
    qr = models.entities.apps.coll.aggregate()
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
        with qmongo.exept_mode("return"):
            entity = models.entities.apps.coll
            actor=entity.where("name=={0}", name)
            actor=actor.push({"views.{0}.roles".format(result.index_of_view): dict(
                role=role,
                is_full_access=is_full_access,
                privileges=privileges
            )})
            ret,ex,msg =actor.commit()
            if ex!=None:
                return None,\
                       lazyobject(ex),\
                       "Add role '{0}' to view '{1}' of app '{2}' is error\n{3]".format(role,view_path,name,msg)
            else:
                return None, \
                       None, \
                       "Add role '{0}' to view '{1}' of app '{2}' is successful".format(role, view_path, name)
    else:
        with qmongo.exept_mode("return"):
            entity = models.entities.apps.coll
            actor = entity.where("name=={0}", name)
            actor = actor.set({
                "views.{0}.roles.{1}".format(result.index_of_view,result.index_of_role):
                    dict(
                        role=role,
                        is_full_access=is_full_access,
                        privileges=privileges
                    )
            })
            ret, ex,msg = actor.commit()
            if ex != None:
                return None, \
                       lazyobject(ex), \
                       "Update role '{0}' to view '{1}' of app '{2}' is error\n{3}".format(role, view_path, name,msg)
            else:
                return None, \
                       None, \
                       "Update role '{0}' to view '{1}' of app '{2}' is successful".format(role, view_path, name)

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
    qr = models.entities.apps.coll.aggregate()
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
        with qmongo.exept_mode("return"):
            entity = models.entities.apps.coll
            actor = entity.where("name=={0}", name)
            actor = actor.pull("views[{0}].roles".format(result.index_of_view)+".role=={0}".format(role))
            ret, ex = actor.commit()
            if ex != None:
                return None, \
                       lazyobject(ex), \
                       "Remove role '{0}' to view '{1}' of app '{2}' is error".format(role, view_path, name)
            else:
                return None, \
                       None, \
                       "Remove role '{0}' to view '{1}' of app '{2}' is successful".format(role, view_path, name)
def role_add_user(role,username):
    role_item =role_get(role)
    if role_item == None:
        return None,lazyobject(
            code="not_found",
            message = "role '{0}' was not found".format(role)
        ),"role '{0}' was not found".format(role)
    entity = models.entities.roles.coll
    qr = models.entities.roles.coll.aggregate()
    qr= qr.match("role=={0}",role)
    qr =qr.project([username],index_of_user="indexOfArray(users,{0})")
    result =qr.get_object()
    if result == None or result.index_of_user==None or result.index_of_user ==-1:
        with qmongo.exept_mode("return"):
            actor=entity.where("role == {0}",role)
            actor=actor.push(users=username)
            ret,ex,message =actor.commit()
            if ex != None:
                return None,lazyobject(ex),"Add user '{1} to role '{0}' is error".format(role,username)
            else:
                return None, None, "Add user '{1}' to role '{0}' is successful".format(role,username)
    else:
        return None, None, "'{0}' is existing in '{1}'".format(username,role)
def schema_get(name):
    return models.entities.schemas.coll.where("schema=={0}",name).object

def schema_create(name,description = None):
    ret = schema_get(name)
    if ret != None:
        return ret,None,"Schema '{0}' is existing".format(name)

    with qmongo.exept_mode("return"):
        entity =  models.entities.schemas
        data = entity.mk_obj()
        data.schema = name
        data.description = description
        ret,ex,msg = entity.insert_one(data)
        if ex != None:
            return None,ex,"Create schema is error,\n {0}".format(msg)
        else:
            return  ret,None,"Create schema is successful"







