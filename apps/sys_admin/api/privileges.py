from .. models.roles import role
import datetime
import validator_params
from quicky import dict_utils
from quicky import api
from .. models import sys_multi_tenancy
from . import format_error
import sys
def get_all_schema(args):
    """
    Get all schema
    :param args:
    :return:
    """
    if not args["privileges"].is_allow_select:
        return {}
    from quicky import applications
    static_schemas=[x.get("schema",None) for x in sys.modules["settings"].APPS if x.get("schema",None) != None]
    dynamic_schema=[x.get("schema",None) for x in sys_multi_tenancy().aggregate().project(schema=1,_id=0).get_list() if x.get("schema",None) != None]
    schema_list=[]
    schema_list.extend(static_schemas)
    schema_list.extend(dynamic_schema)
    return schema_list
def get_list_of_roles(args):
    if not args["privileges"].is_allow_select:
        return {}
    qr=role().aggregate()
    if args["data"].get("schema",None) != None:
        qr.match("schema == {0}",args["data"]["schema"])
    qr.project(
        _id=0,
        id="_id",
        Code="role",
        Schema="schema",
        Name="name",
        Description="description",
        TotalApps="size(apps)"

    )
    data=qr.get_page(page_index=0,page_size=50)
    return data
def insert_role(args):
    if not args["privileges"].is_allow_insert:
        return {}
    ret_validate_require=validator_params.require(["Code", "Name","Schema"], args["data"])
    if ret_validate_require.__len__() > 0:
        msg_require=args["request"].get_app_res("Please enter value of '{0}'");
        field_caption=args["request"].get_app_res("{0}.{1}".format(role().get_name(),ret_validate_require[0],ret_validate_require[0]))
        return dict(
            error=dict(
                msg=msg_require.format(field_caption),
                field=ret_validate_require[0]
            )
        )
    data=dict(
        name=args["data"]["Name"],
        role=args["data"]["Code"],
        schema=args["data"]["Schema"],
        description=args["data"].get("Description",None),
        createdOn=datetime.datetime.now(),
        createdBy=args["request"].user.username,
        apps=[]
    )

    ret=role().insert(data)
    if ret.get("error",None) != None:
        if ret["error"]["code"] == 'missing':
            raise (Exception(ret["error"]["fields"]))
        if ret["error"]["code"] == 'duplicate':
            field=ret["error"]["fields"][0]

    return {}
def get_list_of_applications(args):
    if not args["privileges"].is_allow_select:
        return {}
    qr=role().aggregate()
    if args["data"].get("filter",None) != None:
        if args["data"]["filter"].get("schema",None) != None:
            qr.match("schema == {0}",args["data"]["filter"]["schema"])
        if args["data"]["filter"].get("role",None) != None:
            qr.match("role == {0}", args["data"]["filter"]["role"])
    qr.unwind("apps", False)
    qr.project(
        App="apps.name",
        Description="apps.description",
        CreatedOn="apps.createdOn",
        CreatedBy="apps.createdBy",
        TotalViews="size(apps.views)",
        _id=0
    )
    items=qr.get_list()
    return items
def get_list_of_views(args):
    if not args["privileges"].is_allow_select:
        return {}
    qr=role()
    qr=qr.aggregate()
    qr = qr.unwind("apps", False)
    qr = qr.unwind("apps.views", False)
    if args["data"].get("filter",None) != None:
        if args["data"]["filter"].get("role",None) != None:
            qr.match("role == {0}", args["data"]["filter"]["role"])
        if args["data"]["filter"].get("schema",None) != None:
            qr.match("schema == {0}", args["data"]["filter"]["schema"])
        if args["data"]["filter"].get("app",None) != None:
            qr.match("apps.name == {0}", args["data"]["filter"]["app"])

    qr.project(
        view="apps.views.name",
        description="apps.views.description",
        createdOn="apps.views.createdOn",
        createdBy="apps.views.createdBy",
        totalUser="size(apps.views.users)",
        _id=0
    )
    items=qr.get_list()
    return items
def get_lookup_views(args):
    if not args["privileges"].is_allow_select:
        return {}
    from .. models import views
    qr=views.view().aggregate()
    if args["data"].get("filter",None) != None:
        if args["data"]["filter"].get("app",None) != None:
            qr.match("App == {0}",args["data"]["filter"]["app"])
    qr.project(
        _id =0,
        view="View",
        description="Description"
    )
    qr.sort(view=1)
    items=qr.get_list()
    return items
def add_views_to_app_in_roles(args):
    if not args["privileges"].is_allow_insert:
        return {}
    from quicky import authorize
    app = None
    role = None
    schema =None
    if args["data"].get("filter", None) != None:
        app= args["data"]["filter"].get("app",None)
        role = args["data"]["filter"].get("role", None)
        schema = args["data"]["filter"].get("schema", None)

    for x in args["data"].get("items",[]):
        authorize.add_view_to_role(
            role=role,
            app=app,
            schema=schema,
            view=x.get("view",None)
        )
    return {}
def get_list_of_users_in_role(args):
    if not args["privileges"].is_allow_select:
        return {}
    qr=role().aggregate()
    if args["data"].get("filter",None) != None:
        if args["data"]["filter"].get("role",None) != None:
            qr.match(
                "role=={0} and schema=={1}",
                args["data"]["filter"]["role"],
                args["data"]["filter"]["schema"]
            )
        if args["data"]["filter"].get("app",None) != None:
            qr.unwind("apps", False)
            qr.match("apps.name=={0}",args["data"]["filter"]["app"])
        if args["data"]["filter"].get("view",None) != None:
            qr.unwind("apps.views", False)
            qr.match("apps.views.name=={0}",args["data"]["filter"]["view"])
    qr.unwind("apps.views.users",False)
    qr.project(
        username="apps.views.users.username",
        createdOn="apps.views.users.createdOn",
        createdBy="apps.views.users.createdBy",
        description="apps.views.users.description",
    )
    data=qr.get_page(page_index=args["data"].get("pageIndex",0) ,page_size=args["data"].get("pageSize",50))

    return data
def get_lookup_users(args):
    if not args["privileges"].is_allow_select:
        return {}
    from quicky import tenancy
    schema = tenancy.get_schema()
    if args["data"].get("filter",None) != None:
        schema = args["data"]["filter"].get("schema",schema)
    from .. models import auth_user
    coll= auth_user().switch_schema(schema)
    qr=coll.aggregate()
    qr.project(
        username=1,
        firstName="first_name",
        lastName="last_name",
        isActive="is_active",
        isSupperIser="is_superuser",
        isStaff="is_staff",
        lastLogin="last_login",
        email=1,
        dateJoined="date_joined"
    )
    data=qr.get_page(args["data"].get("pageIndex",0),args["data"].get("pageSize",50))

    return data
def add_users_to_role(args):
    if not args["privileges"].is_allow_insert:
        return {}
    from quicky import authorize
    for x in args["data"].get("items",[]):
        authorize.add_user_to_view(
            role=args["data"]["filter"]["role"],
            app=args["data"]["filter"]["app"],
            schema=args["data"]["filter"]["schema"],
            view=args["data"]["filter"]["view"],
            username=x["username"],
            privileges=args["data"]["privileges"]
        )

    return {}
def get_lookup_apps_list(args):
    if not args["privileges"].is_allow_select:
        return {}
    from quicky import applications
    ret=[]
    for key in list(applications._cache_apps.keys()):
        ret.append( { "name":applications._cache_apps[key].name})
    return ret
def add_apps_to_role(args):
    if not args["privileges"].is_allow_insert:
        return {}
    role_code=args["data"]["filter"]["role"]
    for x in args["data"].get("items",[]):
        qr=role().aggregate()
        qr.unwind("apps",False)
        qr.match("role == {0} and apps.name == {1} and schema=={2}",
                 role_code,
                 x["name"],
                 args["data"]["filter"]["schema"])
        item =qr.get_item()
        if item == None:
            role().push(
                {
                    "apps":{
                        "name":x["name"],
                        "createdBy":args["request"].user.username,
                        "createdOn":datetime.datetime.now(),
                        "views":[]
                    }
                }
            ,"role == {0}",role_code)
    return {}
def get_list_of_schema(args):
    if not args["privileges"].is_allow_select:
        return {}
    from quicky import applications
    from ..models import sys_multi_tenancy
    ret = []
    for key in list(applications._cache_apps.keys()):
        if hasattr(applications._cache_apps[key].settings,"DEFAULT_DB_SCHEMA"):
            ret.append({"schema": applications._cache_apps[key].settings.DEFAULT_DB_SCHEMA})

    items=sys_multi_tenancy().aggregate().project(schema=1,_id=0).get_list()
    ret.extend(items)
    return ret
def get_list_of_users_in_schema(args):
    if not args["privileges"].is_allow_select:
        return {}
    from ..models import auth_user
    qr=auth_user().switch_schema(args["data"]["schema"]).aggregate()
    qr.project(
        _id=0,
        username=1,
        firstName="first_name",
        lastName="last_name",
        isActive="is_active",
        isSuperUser="is_superuser",
        isStaff="is_staff",
        lastLogin='last_login',
        email=1,
        dateJoined="date_joined"
    )
    data=qr.get_page(args["data"].get("pageIndex",0),args["data"].get("pageSize",50))
    return data
def user_manager_add_new_user(args):
    if not args["privileges"].is_allow_insert:
        return {}
    get_app_res=args["request"].get_app_res
    from django.contrib.auth.models import User
    data = args.get("data", {})
    validate_require_result=validator_params.require([
        "username",
        "email",
        "password",
        "schema"
    ],data)
    if validate_require_result.__len__()>0:
        return  dict(
            error=format_error.html_format(validate_require_result,args["request"],args["view"],'missing')
        )
    if data.get("username", None) == None:
        return dict(
            error=dict(
                message=get_app_res("Please enter Username"),
                code="miss_param",
                field="username"
            )
        )
    if data.get("password", None) == None:
        return dict(
            error=dict(
                message=get_app_res("Please enter Password"),
                code="miss_param",
                field="password"
            )
        )
    try:
        user = User.objects.create_user(data.get("username", ""),
                                        data.get("email", data["username"]),
                                        data.get("password", ""),
                                        schema=args["data"]["schema"])
        user.is_superuser = data.get("isSuperUser", False)
        user.is_staff = data.get("isStaff", False)
        user.is_active = data.get("isActive", True)
        user.save(schema=args["data"]["schema"])
    except Exception as ex:
        raise (ex)

    return {}
