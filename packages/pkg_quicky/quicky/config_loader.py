import os
import sys
BASE_DIR = None
import logging
def set_base_dir(value):
    global BASE_DIR
    BASE_DIR =value
def get_params(name):
    import sys
    extra_params = [x for x in sys.argv if x.__len__()>name.__len__()+2 and x[0:2+name.__len__()+1] == "--"+name+"="]
    if extra_params.__len__()==0:
        return None
    else:
        return extra_params[0].split('=')[1]

def load_config(file_name,none_params=False):
    global settings, x
    import imp
    settings = imp.new_module(file_name + ".settings")
    setattr(settings, "BASE_DIR", BASE_DIR)
    import json
    with open(BASE_DIR + os.sep + "configs" + os.sep + file_name + '.json') as f:
        config_from_file = json.load(f)
        if type(config_from_file["APPS"]) in [str,unicode]:
            with open(BASE_DIR + os.sep + "configs" + os.sep + config_from_file["APPS"] + '.json') as f2:
                APPS = json.load(f2)
                config_from_file.update({
                    "APPS":APPS["APPS"]
                })

        for x in config_from_file.get("PACKAGES", []):
            try:
                sys.path.append(BASE_DIR + os.sep + x.replace("/", os.sep))
                print "add path '{0}'".format(BASE_DIR + os.sep + x.replace("/", os.sep))
            except Exception as ex:
                print "add path '{0}' error \n{1}".format(BASE_DIR + os.sep + x.replace("/", os.sep, ex.message))
        configs_items = []
        setattr(settings, "SECRET_KEY", config_from_file["SECRET_KEY"])
        for key in config_from_file.keys():
            try:
                if key == "LOGS":
                    pass
                if key == "PACKAGES":
                    pass
                elif key == "DB_BACK_END":
                    pass
                elif key == "DB_API_CACHE":
                    setattr(settings, key, config_from_file[key])
                elif key == "AUTHORIZATION_ENGINE":
                    setattr(settings, key, config_from_file[key])
                elif key == "DB_AUTH":
                    import quicky

                    quicky.authorize.set_config(config_from_file[key])
                    setattr(settings, key, config_from_file[key])
                elif key == "DB_LANGUAGE":
                    import quicky

                    quicky.language.set_config(config_from_file[key])
                    setattr(settings, key, config_from_file[key])
                elif key == "DB_ENCRYPTOR_CACHE":
                    from . import encryptor

                    encryptor.set_config(config_from_file[key])
                    setattr(settings, key, config_from_file[key])
                elif key == "DB_EXCEL_EXPORT_CONFIG":
                    from . import language

                    language.set_config(config_from_file[key])
                    setattr(settings, key, config_from_file[key])
                elif key == "APPS":
                    pass
                else:
                    setattr(settings, key, config_from_file[key])
                    configs_items.append(key)
                    print "load '{0}' with value {1}".format(key, config_from_file[key])
            except Exception as ex:
                txt_loaded_items = ""
                for x in configs_items:
                    txt_loaded_items = txt_loaded_items + "\n\t\t" + x
                raise (Exception(
                    "load '{0}.json' error, see details:\nloaded items:\n{1}\n error at item:\n '{2}'\n error message:\n{3}".format(
                        file_name, txt_loaded_items, key, ex.message)))
    from django.conf.urls import url, include

    import importlib
    setattr(settings, "AUTHORIZATION_ENGINE", importlib.import_module(config_from_file["AUTHORIZATION_ENGINE"]))
    setattr(settings, "ROOT_URLCONF", 'apps')
    setattr(settings, "STATIC_URL", 'static/')
    setattr(settings, "STATIC_ROOT",
            os.path.join(*(BASE_DIR.split(os.path.sep) + ['apps/static', 'apps/app_main/static'])))
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR + os.sep + config_from_file.get("LOGS", 'logs' + os.sep + 'debug.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
    setattr(settings, "LOGGING", LOGGING)
    sys.modules.update({file_name: {"settings": settings}})
    sys.modules.update({file_name + ".settings": settings})
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", file_name + ".settings")
    # from . import api
    # api.connect(config_from_file["DB_API_CACHE"])
    # from . import backends
    # backends.set_config(config_from_file["DB_BACK_END"])
    from . import url
    url.build_urls(settings.ROOT_URLCONF, [x for x in config_from_file["APPS"] if not x.get("disable", False)])
    from django.core.management import execute_from_command_line
    args = [x for x in sys.argv if x[0:2] != "--"]
    log = logging.getLogger(__file__)
    if not none_params:
        try:
            execute_from_command_line(args)
        except Exception as ex:
            log.debug(ex)
def start_app(name):
    if BASE_DIR == None:
        raise (Exception("It looks like you forgot call 'config_loader.set_base_dir' set root directory of app"))
    import imp
    settings = None
    file_name = get_params(name)
    load_config(file_name)

