VERSION = [1, 0, 0, "beta", 1]


def get_version():
    return VERSION[0].__str__() + \
           "." + VERSION[1].__str__() + \
           "." + VERSION[2].__str__() + \
           "." + VERSION[3].__str__() + \
           "." + VERSION[4].__str__()


class __collections__(object):
    def __init__(self):
        self.__cnn__ = None
        self.__schema__ = None
        self.__my_dict__ = {}

    def set_db(self, cnn):
        self.__cnn__ = cnn
        for key, value in self.__dict__.items():
            if not (key[0:2] == "__" and key[key.__len__() - 2:key.__len__()]) == "__":
                setattr(value, "__db__", self.__cnn__)
        return self

    def set_schema(self, schema):
        self.__schema__ = schema
        for key, value in self.__dict__.items():
            if not (key[0:2] == "__" and key[key.__len__() - 2:key.__len__()]) == "__":
                setattr(value, "__schema__", self.__schema__)
        return self

    def get_cnn(self):
        return self.__cnn__

    def get_schema(self):
        return self.__schema__

    def __setattr__(self, key, value):
        if key[0:2] == "__" and key[key.__len__() - 2:key.__len__()] == "__":
            super(__collections__, self).__setattr__(key, value)
        else:
            setattr(value, "__db__", self.__cnn__)
            setattr(value, "__schema__", self.__schema__)
            super(__collections__, self).__setattr__(key, value)

    def __iter__(self):
        return self.__dict__.items()

        # setattr(item,"__entities__",self)


def auto_load(name, file):
    import importlib
    import imp
    import sys
    import os
    mdl = sys.modules[name]
    def set_db(db):
        mdl.entities.set_db(db)
    def set_schema(schema):
        mdl.entities.set_schema(schema)
    setattr(mdl,"set_db",set_db)
    setattr(mdl, "set_schema", set_db)
    models = importlib.import_module("qmongo.helpers").models
    for x in os.walk(os.path.dirname(file)).next():
        if type(x) is list:
            for f in x:
                if f[f.__len__() - 3:f.__len__()] == ".py":
                    items = f.split(os.sep)
                    file_name = items[items.__len__() - 1]
                    module_name = file_name.split('.')[0]
                    if module_name != "__init__":
                        print "auto load import file {0}".format(f)

                        _mdl = importlib.import_module(name + "." + module_name)
                        model_name = module_name
                        if hasattr(_mdl,"NAME"):
                            model_name = _mdl.NAME
                        if hasattr(models, model_name):
                            m = getattr(models, model_name)
                            if not hasattr(mdl, "entities"):
                                setattr(mdl, "entities", __collections__())
                            colls = getattr(mdl, "entities")
                            setattr(m,"__source_file__",f)
                            setattr(colls, model_name, m)
    import sys
    sys.path.append(os.path.dirname(file)+os.sep+"views")
    for x in os.walk(os.path.dirname(file)+os.sep+"views").next():
        if type(x) is list:
            for f in x:
                if f[f.__len__() - 3:f.__len__()] == ".py":
                    items = f.split(os.sep)
                    file_name = items[items.__len__() - 1]
                    module_name = file_name.split('.')[0]
                    if module_name != "__init__":
                        print "auto load import view from file {0}".format(f)
                        _mdl = importlib.import_module(name + ".views." + module_name)
                        if not hasattr(mdl, "views"):
                            setattr(mdl, "views", __collections__())
                        view_name = module_name
                        colls = getattr(mdl, "views")
                        if hasattr(mdl,"NAME"):
                            view_name = mdl.NAME
                        import qmongo
                        if qmongo.qview._cach_view.has_key(view_name):
                            setattr(qmongo.qview._cach_view[view_name],"__source_file__",f)
                            setattr(colls, view_name, qmongo.qview._cach_view[view_name])
