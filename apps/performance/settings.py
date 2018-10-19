import datetime
from hcs_authorization import authorization
Database=dict(
    host="172.16.7.67",
    name="lms",
    port=27017,
    user="sys",
    password="123456"
)
login_url="login"
authorization.set_db_context_authorization(Database)
def authenticate(request):
    import SystemConfig
    st = SystemConfig.get()
    if request._get_request().has_key("token"):
        token=request._get_request()["token"]
        return_url = request._get_request()["retUrl"]
        lang = request._get_request().get("lang", st.default_language)
        if (lang != None and lang != ""):
            if lang.lower() == "vn":
                lang = "vi"
            else:
                lang = "en"
        from quicky import backends
        import quicky
        from quicky.backends.crypto import sso_authenticate
        from api import models
        login_token = sso_authenticate(token)
        if login_token.is_success:
            login_account = models.auth_user_info().aggregate()\
                .project(login_account = 1, username = 1)\
                .match("login_account == {0}", login_token.login_account).get_item()
            request.__setattr__("user_login", login_account['username'])
            quicky.language.set_language(lang)
            request.session["language"] = lang
            return backends.sigin_by_login_token(request, token, return_url)
        else:
            return False

    if not request.user.is_anonymous() and request.user.is_active:
        return True
    else:
        return False

    # request.user.is_superuser
    # login_info=membership.validate_session(request.session.session_key)
    # if login_info==None:
    #     return False
    # user = login_info.user;
    # if not user.isSysAdmin:
    #     return user.isStaff
    # else:
    #     return True

def AUTHORIZED(func_id):
    from api import models
    exist = models.AD_Roles().aggregate()\
    .unwind("permission", False)\
    .project(
        function_id = "permission.function_id"
    )\
    .match("function_id == {0}", func_id).get_item()

    if exist != None:
        return True
    return False

def on_begin_request(request):
    setattr(request,"begin_time",datetime.datetime.now())
    print(request)

def on_end_request(request):
    print("time is :{0} in {1}".format((datetime.datetime.now()-request.begin_time).microseconds,request.path_info))
