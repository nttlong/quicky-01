import logging

class __collections__(object):
    pass
def load(name,file):
    logging.basicConfig(filename='logs/model.log', level=logging.DEBUG)
    try:
        import importlib
        import imp
        import sys
        import os
        mdl= sys.modules[name]
        models = importlib.import_module("qmongo.helpers").models
        for x in os.walk(os.path.dirname(file)).next():
            if type(x) is list:
                for f in x:
                    if  f[f.__len__()-3:f.__len__()]==".py":
                        items=f.split(os.sep)
                        file_name=items[items.__len__()-1]
                        module_name = file_name.split('.')[0]
                        if module_name != "__init__":
                            print "auto load import file {0}".format(f)
                            _mdl= None
                            try:
                                mdl=importlib.import_module(name+"."+module_name)
                                logging.info("auto load import file {0}".format(f))
                            except Exception as ex:
                                logging.debug("import file {0} is error".format(f),ex)
                                raise Exception(dict(
                                    message="import file {0} is error".format(os.path.dirname(file)+"/"+f),
                                    error=ex
                                ))
                            if hasattr(models,module_name):
                                try:
                                    m= getattr(models,module_name)
                                    if not hasattr(mdl,"entities"):
                                        setattr(mdl,"entities",__collections__())
                                    colls = getattr(mdl,"entities")
                                    setattr(colls, module_name, m)
                                    logging.info("create '{0}' model from file '{1}' is ok",module_name,f)
                                except Exception as ex:
                                    raise Exception(dict(
                                        message="import file {0} is error".format(f),
                                        error=ex
                                    ))
                                    raise ex
    except Exception as ex:
        logging.debug(ex)
        raise ex

