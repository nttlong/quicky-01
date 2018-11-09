def load_controllers(name,file):
    """
    This method allow load view into views.py ex:
    load_views(__name__,__file__)

    :param name:
    :param file:
    :return:
    """
    import importlib
    import imp
    import sys
    import os
    from inspect import getmembers, isfunction
    import quicky.executor
    mdl = sys.modules[name]
    dir_of_controllers=os.path.dirname(file)
    for x in os.walk(dir_of_controllers).next():
        if type(x) is list:
            for f in x:
                if f[f.__len__() - 3:f.__len__()] == ".py":
                    items = f.split(os.sep)
                    file_name = items[items.__len__() - 1]
                    module_name = file_name.split('.')[0]
                    if module_name != "__init__":
                        print "auto load import file {0}".format(f)
                        _mdl = importlib.import_module(name + "." + module_name)
                        functions_list = [o for o in getmembers(_mdl) if
                                          hasattr(o[1], 'im_class') and o[1].im_class is quicky.executor.executor]
                        for fn in functions_list:
                            setattr(mdl,fn[0],fn[1])
