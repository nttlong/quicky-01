import  threading
import sys
from . import extens
import tenancy
__schema_cache__ = {}
__apps_cache__ = {}
class executor(object):
    def __init__(self,fn,path):

        has_set_schema = False
        from . import applications as apps
        self.__app__ = None
        self.__fn__ = fn
        self.__path_fn__= path
        if sys.version_info[0] <= 2:
            self.__app__ = apps.get_app_by_file(self.__fn__.func_code.co_filename)
        else:
            self.__app__ = apps.get_app_by_file(self.__fn__.__code__.co_filename)
        if self.__app__ != None:
            if hasattr(self.__app__.settings, "DEFAULT_DB_SCHEMA") and not has_set_schema:
                tenancy.set_schema(self.__app__.settings.DEFAULT_DB_SCHEMA)
    def load_app(self,request):
        if __apps_cache__.has_key(request.path):
            self.__app__ = __apps_cache__[request.path]
        import applications
        from django.conf import settings
        path = request.path
        path = path[1:path.__len__()]
        if settings.HOST_DIR!="":
            path = path[settings.HOST_DIR.__len__():path.__len__()]
        if path.__len__()>3 and path[path.__len__()-3:path.__len__()] =="api":
            path = path[0:path.__len__() - 3]
            items = path.split('/')
            if items[1] == '':
                self.__app__ = applications.get_app_by_host_dir(items[1])
                __apps_cache__.update({request.path:self.__app__})

    def get_schema(self,request):
        import tenancy
        if __schema_cache__.has_key(request.path):
            return __schema_cache__[request.path]
        if self.__app__.is_persistent_schema():
            from django.conf import settings
            return self.__app__.get_persistent_schema()
        elif self.__app__.host_dir == "":
            return settings.MULTI_TENANCY_DEFAULT_SCHEMA
        elif settings.HOST_DIR != "":
            path = request.path
            if path[0] == '/':
                path =path[1:path.__len__()]
            path = path[settings.HOST_DIR.__len():path.__len__()]
            if path[0] == '/':
                path =path[1:path.__len__()]
            items =path.split('/')
            __schema_cache__.update({
                request.path:tenancy.get_schema(items[0])
            })
            return __schema_cache__[request.path]
    def exec_request(self, request, **kwargs):
        if self.__app__ == None:
            self.load_app(request)
        schema =self.get_schema(request)
        tenancy.set_schema(schema)

        # from . import language
        setattr(threading.current_thread(), "user", request.user)
        setattr(threading.currentThread(), "user", request.user)
        # print(request.session.session_key)

        from django.conf import settings
        if settings==None:
            from . import get_django_settings_module
            settings=get_django_settings_module()
        host_dir=None
        if hasattr(settings,"HOST_DIR"):
            host_dir=settings.HOST_DIR
        app=self.__app__

        # try:
        from django.shortcuts import redirect
        not_inclue_tenancy_code=False
        if hasattr(request,"not_inclue_tenancy_code"):
            not_inclue_tenancy_code=request.not_inclue_tenancy_code
        is_allow = True
        is_public = False
        authenticate = None
        request_path=request.path
        if host_dir != None:
            request_path = request_path[host_dir.__len__()+1:request_path.__len__()]
        tenancy_code=tenancy.get_customer_code()
        if not not_inclue_tenancy_code and tenancy_code!=None:
            request_path=request_path[tenancy_code.__len__()+1:request_path.__len__()]
        if app == None:
            x=1

        if app==None and request_path[request_path.__len__() - 4:request_path.__len__()]=="/api":
            app_name=request_path.split('/')[request_path.split('/').__len__()-2]
            if app_name==tenancy_code:
                app_name=""
            if hasattr(settings,"HOST_DIR") and settings.HOST_DIR.lower() == app_name.lower():
                app_name = ""
            from . import applications
            app=applications.get_app_by_name(app_name)
            if app != None and not has_set_schema:
                if hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
                    tenancy.set_schema(app.settings.DEFAULT_DB_SCHEMA)
                else:
                    from . import get_tenancy_schema
                    _tenancy_code=request_path.split('/')[1]
                    _schema=get_tenancy_schema(request_path.split('/')[1])

                    setattr(threading.currentThread(), "tenancy_code", _tenancy_code)
                    setattr(threading.currentThread(), "request_tenancy_code", _schema)
                    setattr(request, "tenancy_code", _schema)


            else:
                from django.conf import settings as g_settings
                if g_settings.MULTI_TENANCY_DEFAULT_SCHEMA == app_name:
                    app = applications.get_app_by_host_dir("")
                    if app != None and not has_set_schema:

                        setattr(threading.currentThread(),"tenancy_code",app_name)
                        setattr(threading.currentThread(),"request_tenancy_code",app_name)
                        setattr(request,"tenancy_code",app_name)
                else:
                    app = applications.get_app_by_host_dir(app_name)
                    if app != None and not has_set_schema:
                        tenancy_code=request_path.split('/')[1];

                        setattr(threading.currentThread(),"tenancy_code",tenancy_code)
                        setattr(threading.currentThread(),"request_tenancy_code",tenancy_code)
                        setattr(request,"tenancy_code",tenancy_code)
                        if hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
                            tenancy.set_schema(app.settings.DEFAULT_DB_SCHEMA)
                            setattr(request, "tenancy_code", app.settings.DEFAULT_DB_SCHEMA)



        if not hasattr(app, "settings") or app.settings==None:
            raise (Exception("'settings.py' was not found in '{0}' at '{1}' or look like you forgot to place 'import settings' in '{1}/__init__.py'".format(app.name, os.getcwd()+os.sep+app.path)))



        if hasattr(app.settings, "is_public"):
            is_public = getattr(app.settings, "is_public")

        # if not is_public or callable(authenticate):

        extens.apply(request, self.__path_fn__, app)
        if type(self.__path_fn__) is dict:
            if self.__path_fn__.get("is_public", False):
                return self.__fn__(request, **kwargs)
            elif self.__path_fn__.get("login_url", None) != None:
                if app.host_dir != "":
                    login_url = "/" + app.host_dir + "/" + self.__path_fn__["login_url"]
                else:
                    login_url = "/" + self.__path_fn__["login_url"]
        if hasattr(app.settings, "authenticate"):
            from django.http.response import HttpResponseRedirect

            ret_auth=app.settings.authenticate(request)
            login_url = self.__app__.get_login_url()


            if ret_auth != True:

                if ret_auth == False:
                    if login_url==None:
                        raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                    cmp_url=login_url

                    if request.path_info.lower() == login_url.lower():
                        return self.__fn__(request, **kwargs)
                    url = request.get_abs_url() + login_url
                    _request_path = request.path
                    if _request_path[0] == '/':
                        _request_path = _request_path[1:_request_path.__len__()]
                    if _request_path.__len__() > 0 and _request_path[_request_path.__len__()-1] == '/':
                        _request_path = _request_path[0:_request_path.__len__()-1]

                    if host_dir != None:
                        _request_path = _request_path[host_dir.__len__():_request_path.__len__()]

                    url += "?next=" + request.get_abs_url() + "/"+_request_path
                    return redirect(url)
            elif type(ret_auth) is HttpResponseRedirect:
                return ret_auth
        from django.conf import settings as st
        # lang = request.session.get('language', st.LANGUAGE_CODE)
        from . import language

        language.set_language("vi")
        import qtracking
        if request.get_view_path()!="api":
            qtracking.track_load_page(app.name,tenancy.get_schema(),request.get_view_path(),request.user.username)
            return self.__fn__ (request, **kwargs)
        else:
            ret_id=qtracking.track_call_api_before(app.name,tenancy.get_schema(), request.body, request.user.username)
            ret_data = self.__fn__(request, **kwargs)
            qtracking.track_call_api_after(app.name,tenancy.get_schema(),ret_id,ret_data.content,request.user.username)
            return ret_data
        # except Exception as ex:
        #     logger.debug(ex)
        #     raise (ex)
    def exec_request_for_multi(self,request,tenancy_code, **kwargs):

        from . import get_tenancy_schema
        code=get_tenancy_schema(tenancy_code)
        if code==None:
            from django.http import HttpResponse, HttpResponseNotFound
            return HttpResponseNotFound("Page not found")
        setattr(threading.current_thread(),"tenancy_code",code)
        setattr(threading.currentThread(), "tenancy_code", code)
        setattr(threading.current_thread(),"request_tenancy_code",tenancy_code)
        setattr(threading.currentThread(), "request_tenancy_code", tenancy_code)
        setattr(threading.current_thread(),"user",request.user)
        setattr(threading.currentThread(), "user", request.user)
        from django.conf import settings as st
        from . import language
        lang = request.session.get('language', st.LANGUAGE_CODE)
        language.set_language(lang)
        return self.exec_request(request,**kwargs)
    def execute_request(self,is_multi_tenancy):
        if is_multi_tenancy:
            if self.__app__ == None:
                return self.exec_request
            elif hasattr(self.__app__.settings, "DEFAULT_DB_SCHEMA"):
                if self.__app__.host_dir == "":
                    return self.exec_request
                else:
                    return self.exec_request
            else:
                return self.exec_request_for_multi
        else:
            return self.exec_request