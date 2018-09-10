from .. import dict_utils
from .. import language as lang_manager
from .. import api
from django.core.context_processors import csrf
import threading
global __apps_cache__
global __schema_cache__
global __customer__code__
global __view_path__
global _abs_urls
global _language_cache
global lock
global __app_host__
_language_cache = {}
_abs_urls = {}
__apps_cache__ = {}
__schema_cache__ ={}
__customer__code__ = {}
__view_path__ = {}
lock=threading.Lock()
__app_host__ = {}
def __remove_first__(x,y):
    if y== None or y == "":
        return y
    else:
        while y!="" and y[0]==x:
            y=y[1:y.__len__()]
        return y
def __remove_last__(x,y):
    if y== None or y == "":
        return y
    else:
        while y!="" and y[y.__len__()-1]==x:
            y=y[0:y.__len__()-1]
        return y
def get_language_item(schema,language,app_name,view,key,value):

    hash_key="schema={4},language={0};app={1};view={2};key={3}".format(language,app_name,view,key,schema).lower()
    if not dict_utils.has_key(_language_cache,hash_key):
        try:
            lock.acquire()
            ret=lang_manager.get_language_item(schema,language,app_name,view,key,value)
            _language_cache[hash_key]=ret
            lock.release()
        except Exception as ex:
            lock.release()
            raise ex
    return _language_cache[hash_key]
class extension(object):
    def __str_trim__(self,_str_):
        if _str_ == "":
            return ""
        while _str_.__len__()>0 and _str_[0] == '/':
            _str_ = _str_[1:_str_.__len__()]
        while _str_.__len__()>0 and _str_[_str_.__len__() - 1] == '/':
            _str_ = _str_[0:_str_.__len__() - 1]
        while _str_.__len__()>0 and _str_.count("//") > 0:
            _str_ = _str_.replace("//", "/")
        return _str_
    def init_app(self,request):
        from .. import applications
        from django.conf import settings
        if hasattr(request,"__app__") and request.__app__ !=-1:
            return

        if __apps_cache__.has_key(request.path):
            setattr(request,"__app__",__apps_cache__[request.path])
        path = request.path
        path = path[1:path.__len__()]
        if hasattr(settings,"HOST_DIR") and settings.HOST_DIR!="":
            path = path[settings.HOST_DIR.__len__():path.__len__()]
        if path == "api":
            setattr(request,"__app__",applications.get_app_by_host_dir(""))
            __apps_cache__.update({request.path: request.__app__})
            return
        elif path[path.__len__()-4:path.__len__()] == "/api":
            path = path[0:path.__len__() - 4]
        items = path.split('/')

        if items.__len__()>1:
            app = applications.get_app_by_host_dir(items[1])
        else:
            app = applications.get_app_by_host_dir(items[0])
        if app ==-1:
            app = applications.get_app_by_host_dir("")

        setattr(request,"__app__",app)
        __apps_cache__.update({request.path: app})
    def init_customer_code(self,request):
        from django.conf import settings
        if __customer__code__.has_key(request.path) and __customer__code__.has_key(request.path) !="":
            return
        if request.__app__.is_persistent_schema():
            __customer__code__.update({
                request.path: None
            })

        elif request.__app__.host_dir == "":
            path =self.__str_trim__(request.path)

            if hasattr(settings,"HOST_DIR") and settings.HOST_DIR != "":
                if path.__len__()>settings.HOST_DIR.__len__():
                    path = self.__str_trim__(path[settings.HOST_DIR.__len__():path.__len__()])
                else:
                    __customer__code__.update({
                        request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
                    })
                    return

            items = path.split('/')

            if items.__len__()>0:
                __customer__code__.update({
                    request.path: items[0]
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
            path = path[0:path.__len__() -self.__app__.host_dir.__len__()]
            if path[0] == '/':
                path = path[1:path.__len__()]
            items = path.split('/')

            if items.__len__() > 1:
                __customer__code__.update({
                    request.path: items[0]
                })
            else:
                __customer__code__.update({
                    request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
                })
    def get_abs_url(self,request):

        __root_url__= None
        host_dir = None
        from django.conf import settings

        if hasattr(settings, "HOST_DIR"):
            host_dir = settings.HOST_DIR
        if host_dir==None:
            if dict_utils.has_key(_abs_urls, request.get_host()):
                return _abs_urls[request.get_host()]
            if request.get_full_path() == "/":
                __root_url__ = request.build_absolute_uri()
            else:
                __root_url__ = request.build_absolute_uri().replace(
                    request.get_full_path(), "")
            if __root_url__[__root_url__.__len__() - 1] == "/":
                __root_url__ = __root_url__[0:__root_url__.__len__() - 1]
            _abs_urls.update({
                request.get_host():__root_url__
            })
            return __root_url__
        else:
            if dict_utils.has_key(_abs_urls, request.get_host()+"/"+host_dir):
                return _abs_urls[request.get_host()+"/"+host_dir]


            if request.get_full_path() == "/":
                __root_url__ = request.build_absolute_uri()
            else:
                __root_url__ = request.build_absolute_uri().replace(
                    request.get_full_path(), "")
            if __root_url__[__root_url__.__len__() - 1] == "/":
                __root_url__ = __root_url__[0:__root_url__.__len__() - 1]
            __root_url__ = __root_url__ + "/" + host_dir
            _abs_urls.update({
                request.get_host() + "/" + host_dir: __root_url__
            })
            return __root_url__

    def init_schema(self,request):
        from .. import tenancy
        from .. import get_tenancy_schema
        from django.conf import settings
        if __schema_cache__.has_key(request.path) \
                and __schema_cache__[request.path] !=None\
                and __schema_cache__[request.path]!="":
            return __schema_cache__[request.path]
        if request.__app__.is_persistent_schema():
            __schema_cache__.update({
                request.path:request.__app__.get_persistent_schema()
            })
        elif request.__customer_code__ =="":
            from .. import get_tenancy_schema
            __schema_cache__.update({
                request.path: settings.MULTI_TENANCY_DEFAULT_SCHEMA
            })
        else:
            from .. import get_tenancy_schema
            __schema_cache__.update({
                request.path:get_tenancy_schema(request.__customer_code__)
            })

        return __schema_cache__[request.path]
    def apply(self,request):
        def get_language():
            """
            get language of current session
            :return:
            """
            from django.conf import settings as st
            from django.utils import translation
            return request.session.get('language', st.LANGUAGE_CODE)
            return "vi"
        #--------------------------------------------------------------

        def set_language(lang):
            """
            set current language for request
            :param lang:
            :return:
            """
            # from django.utils.translation import activate
            # activate(lang)
            request.session['language'] = lang
            from .. import language
            language.set_language(lang)
        #--------------------------------------------------------------
        def get_language_name():
            """
            get language name of current language
            :return:
            """
            from django.conf import settings
            items = [x for x in settings.LANGUAGES if x[0] == get_language()]
            if items.__len__() > 0:
                return items[0][1]
            return "NA"
        #------------------------------------------------------------
        def get_languages():
            from django.conf import settings
            if not hasattr(settings, "LANGUAGES"):
                raise (Exception("It looks like you forgot set LANGUAGES in settings.py"))
            ret = []
            for x in settings.LANGUAGES:
                ret.append({
                    "code": x[0],
                    "name": x[1]
                })
            return ret
        #------------------------------------------------------------
        def get_schema():
            return __schema_cache__[request.path]
        #-----------------------------------------------------------
        def get_customer_code():
            return request.__customer_code__
        #-----------------------------------------------------------
        def get_app():
            return request.__app__
        #----------------------------------------------------------
        def get_abs_url():
            return self.get_abs_url(request)
        #-----------------------------------------------------------
        def get_app_host():
            from  .. import tenancy
            if __app_host__.has_key(request.path):
                return __app_host__[request.path]

            app =request.get_app()
            from django.conf import settings
            is_multi_tenancy = settings.USE_MULTI_TENANCY
            if not is_multi_tenancy:
                __app_host__.update({
                    request.path:app.host_dir
                })
                return app.host_dir
            else:
                if not app.is_persistent_schema():
                    if app.host_dir == "":
                        __app_host__.update({
                            request.path: request.get_customer_code()
                        })
                        return request.get_customer_code()
                    else:
                        __app_host__.update({
                            request.path: tenancy.get_customer_code() + "/" + app.host_dir
                        })
                        return tenancy.get_customer_code() + "/" + app.host_dir
                else:
                    if app.host_dir == "":
                        __app_host__.update({
                            request.path: ""
                        })
                        return ""
                    else:
                        __app_host__.update({
                            request.path: app.host_dir
                        })
                        return app.host_dir
        #-----------------------------------------------------------
        def get_app_url(path):
            if get_app_host() == "":
                return get_abs_url() + (lambda: "" if path == "" else "/" + path)()
            else:
                return (get_abs_url() + "/" + get_app_host() + (lambda: "" if path == "" else "/" + path)())
        #-----------------------------------------------------------------
        def get_view_path():
            from django.conf import settings
            if __view_path__.get(request.path,None)!=None:
                return __view_path__[request.path]
            from  .. import tenancy
            app =request.get_app()
            if hasattr(request, "__view_path"):
                if request.__view_path == "":
                    request.__view_path = "index"
                __view_path__.update({
                    request.path:request.__view_path
                })
                return request.__view_path
            code = request.get_schema()
            not_inclue_tenancy_code = False
            if hasattr(request, "not_inclue_tenancy_code"):
                not_inclue_tenancy_code = request.not_inclue_tenancy_code
            ret = request.get_full_path().split("?")[0]
            ret = __remove_last__("/", __remove_first__("/", ret))
            if hasattr(settings,"HOST_DIR"):
                if ret.lower() == settings.HOST_DIR.lower():
                    __view_path__.update({
                        request.path: "index"
                    })
                    setattr(request, "__view_path", "index")
                    return "index"
                if ret.lower().find(settings.HOST_DIR.lower()+"/")==0:
                    ret = ret[settings.HOST_DIR.__len__():ret.__len__()]
            if app.name == "default" or app.host_dir == "":
                ret = __remove_last__("/", __remove_first__("/", ret))

                if ret == "":
                    __view_path__.update({
                        request.path:  "index"
                    })
                    setattr(request, "__view_path", "index")
                    return "index"
                else:
                    if not app.is_persistent_schema():
                        if code == None:
                            return  None
                        if ret.lower().find(code.lower()+"/")==0:
                            ret= ret[code.__len__()+1:ret.__len__()]
                            ret = __remove_last__("/", __remove_first__("/", ret))
                            setattr(request, "__view_path", ret)
                            __view_path__.update({
                                request.path: ret
                            })
                            return ret
                        else:
                            ret = __remove_last__("/", __remove_first__("/", ret))
                            setattr(request, "__view_path", ret)
                            __view_path__.update({
                                request.path: ret
                            })
                            return ret
                    else:
                        ret = (lambda x: x if x != "" else "index")(ret)
                        ret = __remove_last__("/", __remove_first__("/", ret))
                        __view_path__.update({
                            request.path: ret
                        })
                        return ret
            else:
                if app.is_persistent_schema():
                    ret = __remove_last__("/", __remove_first__("/", ret))
                    ret = ret[app.host_dir.__len__():ret.__len__()]
                    ret = __remove_last__("/", __remove_first__("/", ret))

                    if ret == "":
                        setattr(request, "__view_path", "index")
                        __view_path__.update({
                            request.path: "index"
                        })
                        return "index"
                    else:
                        __view_path__.update({
                            request.path:ret
                        })
                        setattr(request, "__view_path", ret)
                        return ret
                else:
                    ret = __remove_last__("/", __remove_first__("/", ret))

                    ret = ret[code.__len__():ret.__len__()]

                    ret = __remove_last__("/", __remove_first__("/", ret))

                    ret = ret[app.host_dir.__len__():ret.__len__()]

                    ret = __remove_last__("/", __remove_first__("/", ret))
                    if ret == "":
                        __view_path__.update({
                            request.path: "index"
                        })
                        setattr(request, "__view_path", "index")
                        return "index"
                    else:
                        __view_path__.update({
                            request.path: ret
                        })
                        setattr(request, "__view_path", ret)
                        return ret
        #------------------------------------------------------------------
        def get_res(value,key=None):
            if value == None:
                value = key
            key = key.lower()
            return get_language_item(request.get_schema(), get_language(), request.get_app().name, get_view_path(), key, value)
        #------------------------------------------------------------------
        def get_app_res(key, value=None):
            if value == None:
                value = key
            key = key.lower()
            return get_language_item(request.get_schema(), get_language(), request.get_app().name, "-", key, value)
        #-------------------------------------------------------------------
        def get_global_res(key, value=None):
            if value == None:
                value = key
            key = key.lower()
            return get_language_item(request.get_schema(), get_language(), "-", "-", key, value)
        #---------------------------------------------------------------------
        def get_static(path):
            app = request.get_app()
            if app.host_dir=="":
                return get_abs_url()+"/"+app.name+"/static" + "/" + path
            else:
                return get_abs_url()+"/"+app.host_dir+"/"+"static/"+path
        #---------------------------------------------------------------------
        def get_app_name():
            return request.get_app().name
        #---------------------------------------------------------
        def get_api_key(path):
            items = path.split('.')
            if items.__len__() > 2:
                path = path[items[0].__len__():path.__len__()]
            else:
                path = "." + path
            return api.get_api_key(request.get_app().mdl.__name__ + path)
        #-----------------------------------------------------------
        def get_api_path(id):
            return api.get_api_path(id)
        #-----------------------------------------------------------
        def get_csrftoken():
            if type(csrf(request)["csrf_token"]) is str:
                return csrf(request)["csrf_token"]
            else:
                return csrf(request)["csrf_token"].encode()
        #-----------------------------------------------------------
        def get_login_url():
            return request.__app__.get_login_url(request.get_customer_code())
        #-----------------------------------------------------------
        extends_functions =[
            get_language,
            set_language,
            get_language_name,
            get_languages,
            get_schema,
            get_customer_code,
            get_abs_url,
            get_app_host,
            get_app_url,
            get_app,
            get_view_path,
            get_res,
            get_app_res,
            get_global_res,
            get_static,
            get_app_name,
            get_api_key,
            get_api_path,
            get_csrftoken,
            get_login_url
        ]
        setattr(request,"__fn__",{})
        _fn_=getattr(request,"__fn__")
        for fn in extends_functions:
            setattr(request,fn.func_name,fn)
            _fn_.update({
                fn.func_name:fn
            })

    def process_request(self,request):
        self.init_app(request)
        self.init_customer_code(request)
        setattr(request,"__customer_code__",__customer__code__[request.path])
        self.init_schema(request)
        self.apply(request)
