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
        return self.__my_dict__.items()

        # setattr(item,"__entities__",self)


def auto_load(name, file):
    import importlib
    import imp
    import sys
    import os
    mdl = sys.modules[name]
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
                        if hasattr(models, module_name):
                            m = getattr(models, module_name)
                            if not hasattr(mdl, "entities"):
                                setattr(mdl, "entities", __collections__())
                            colls = getattr(mdl, "entities")
                            setattr(colls, module_name, m)
