VERSION = [1,0,0,"beta",1]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
def create_model(name,required,indexes,fields):
    """
    :param name:
    :param indexes:
    :param fields:
    :return:

    """
    import pymodel
    # type: (str,object, list(pymodel.Index), object) -> object
    return pymodel.create_model(name,required,indexes,fields)
def query(*args,**kwargs):
    # type: (object, object) -> pyquery.query
    """

    :param args:
    :param kwargs:
    :return:
    create queryable for monongodb with aggregate pipeline support and CRUID opreator
    """
    import pyquery
    return pyquery.query(*args,**kwargs)
def documents():
    import pydoc
    return pydoc.Fields()
def mongodb_functions():
    import pyfuncs
    return pyfuncs
def compile(exr):
    """
    :rtype: dict
    """
    import pydoc
    if not isinstance(exr,pydoc.Fields):
        raise Exception("invalid data type")
    return exr.__tree__
funcs=mongodb_functions()
doc=documents()
from pymodel import Index,IndexOption,FieldInfo
def create_index(fields,options):
    import pymodel
    return pymodel.Index(fields,options)
