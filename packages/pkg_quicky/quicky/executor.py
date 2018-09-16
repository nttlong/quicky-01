import  threading
import sys
from . import extens
import tenancy
import logging
import urllib
__schema_cache__ = {}
__customer__code__ ={}
__apps_cache__ = {}
__log__ = logging.getLogger(__name__)

__mdl__ = None
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
    def exec_request(self, request, **kwargs):
        try:
            return self.run_request(request,**kwargs)
        except Exception as ex:
            __log__.debug(ex.message,ex)
            raise ex


    def run_request(self, request, **kwargs):
        global  __mdl__
        if __mdl__ == None:
            from . import middleware
            __mdl__ =  middleware.extension()

        __mdl__.process_request(request)

        schema =request.get_schema()
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
        if hasattr(request.get_app().settings, "authenticate"):
            from django.http.response import HttpResponseRedirect
            ret_auth=request.get_app().settings.authenticate(request)
            login_url = request.get_login_url()
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
            qtracking.track_load_page(request.get_app().name,tenancy.get_schema(),request.get_view_path(),request.user.username)
            return self.__fn__ (request, **kwargs)
        else:
            ret_id=qtracking.track_call_api_before(request.get_app().name,tenancy.get_schema(), request.body, request.user.username)
            ret_data = self.__fn__(request, **kwargs)
            qtracking.track_call_api_after(request.get_app().name,tenancy.get_schema(),ret_id,ret_data.content,request.user.username)
            return ret_data
        # except Exception as ex:
        #     logger.debug(ex)
        #     raise (ex)
    def exec_request_for_multi(self,request,tenancy_code, **kwargs):
        global __mdl__
        if __mdl__ == None:
            from . import middleware
            __mdl__ = middleware.extension()

        __mdl__.process_request(request)
        from . import get_tenancy_schema
        code=request.get_schema()
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
    def process_request(selfs,request):
        print "OK"