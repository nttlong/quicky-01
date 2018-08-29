import  threading
import sys
from . import extens
import tenancy
__schema_cache__ = {}
__customer__code__ ={}
__apps_cache__ = {}
class executor(object):
    def __init__(self,fn,path):
        if type(path) is dict:
            x=1

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
        if self.__app__ !=None:
            return
        if __apps_cache__.has_key(request.path):
            self.__app__ = __apps_cache__[request.path]
        import applications
        from django.conf import settings
        path = request.path
        path = path[1:path.__len__()]




        if hasattr(settings,"HOST_DIR") and settings.HOST_DIR!="":
            path = path[settings.HOST_DIR.__len__():path.__len__()]
        if path == "api":
            self.__app__ =applications.get_app_by_host_dir("")
            __apps_cache__.update({request.path: self.__app__})
            return
        elif path[path.__len__()-4:path.__len__()] == "/api":
            path = path[0:path.__len__() - 4]
        items = path.split('/')

        if items.__len__()>1:
            app = applications.get_app_by_host_dir(items[1])
        else:
            app = applications.get_app_by_host_dir(items[0])
        if app ==-1:
            app = applications.get_app_by_host_dir(items[0])

        self.__app__ = app
        __apps_cache__.update({request.path: self.__app__})






    def get_customer_code(self,request):
        from django.conf import settings
        if __customer__code__.has_key(request.path):
            return __customer__code__[request.path]
        if self.__app__.is_persistent_schema():
            __customer__code__.update({
                request.path: None
            })

        elif self.__app__.host_dir == "":
            path = request.path
            if path[0] == '/':
                path = path[1:path.__len__()]
            if hasattr(settings,"HOST_DIR") or settings.HOST_DIR != "":
                path = path[settings.HOST_DIR.__len__():path.__len__()]
            items = path.split('/')

            if items.__len__()>1:
                __customer__code__.update({
                    request.path: items[1]
                })
            else:
                __customer__code__.update({
                    request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
                })
        else:
            path = request.path
            if path[0] == '/':
                path = path[1:path.__len__()]
            if hasattr(settings,"HOST_DIR") and settings.HOST_DIR != "":
                path = path[settings.HOST_DIR.__len__():path.__len__()]
            path = path[self.__app__.host_dir.__len__():path.__len__()]
            items = path.split('/')

            if items.__len__() > 1:
                __customer__code__.update({
                    request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
                })
            else:
                __customer__code__.update({
                    request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
                })
        return __customer__code__[request.path]

    def get_schema(self,request):
        import tenancy
        from . import get_tenancy_schema
        from django.conf import settings
        if __schema_cache__.has_key(request.path):

            return __schema_cache__[request.path]
        if self.__app__.is_persistent_schema():
            __schema_cache__.update({
                request.path:self.__app__.get_persistent_schema()
            })
        else:
            from . import get_tenancy_schema
            __schema_cache__.update({
                request.path:(lambda x,y: y if x==None else x)(settings.MULTI_TENANCY_DEFAULT_SCHEMA,get_tenancy_schema(self.get_customer_code(request)))
            })

        return __schema_cache__[request.path]
    def exec_request(self, request, **kwargs):
        import urllib
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

        # if not is_public or callable(authenticate):

        extens.apply(request, self.__path_fn__, self.__app__)
        if type(self.__path_fn__) is dict:
            if self.__path_fn__.get("is_public", False):
                return self.__fn__(request, **kwargs)
            elif self.__path_fn__.get("login_url", None) != None:
                if self.__app__.host_dir != "":
                    login_url = "/" + self.__app__.host_dir + "/" + self.__path_fn__["login_url"]
                else:
                    login_url = "/" + self.__path_fn__["login_url"]
        if hasattr(self.__app__.settings, "authenticate"):
            from django.http.response import HttpResponseRedirect

            ret_auth=self.__app__.settings.authenticate(request)
            login_url = self.__app__.get_login_url(self.get_customer_code(request))


            if ret_auth != True:

                if ret_auth == False:
                    if login_url==None:
                        raise (Exception("it look like you forgot set 'login_url' in {0}/settings.py".format(app.path)))
                    cmp_url=request.build_absolute_uri().split('?')[0]
                    if cmp_url[cmp_url.__len__()-1] == '/':
                        cmp_url = cmp_url[0:cmp_url.__len__()-1]

                    if cmp_url.lower().replace('//','/') == (request.get_abs_url()+"/"+login_url).replace('//','/').lower():
                        return self.__fn__(request, **kwargs)
                    url = request.get_abs_url() + ("/"+login_url).replace("//","/")

                    _request_path = request.path
                    if _request_path[0] == '/':
                        _request_path = _request_path[1:_request_path.__len__()]
                    if _request_path.__len__() > 0 and _request_path[_request_path.__len__()-1] == '/':
                        _request_path = _request_path[0:_request_path.__len__()-1]

                    if host_dir != None:
                        _request_path = _request_path[host_dir.__len__():_request_path.__len__()]


                    url += "?next=" + urllib.quote_plus(request.get_abs_url() + ("/"+_request_path).replace("//","/"))
                    return redirect(url)
            elif type(ret_auth) is HttpResponseRedirect:
                return ret_auth
        from django.conf import settings as st
        # lang = request.session.get('language', st.LANGUAGE_CODE)
        from . import language

        language.set_language("vi")
        import qtracking
        if request.get_view_path()!="api":
            qtracking.track_load_page(self.__app__.name,tenancy.get_schema(),request.get_view_path(),request.user.username)
            return self.__fn__ (request, **kwargs)
        else:
            ret_id=qtracking.track_call_api_before(self.__app__.name,tenancy.get_schema(), request.body, request.user.username)
            ret_data = self.__fn__(request, **kwargs)
            qtracking.track_call_api_after(self.__app__.name,tenancy.get_schema(),ret_id,ret_data.content,request.user.username)
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