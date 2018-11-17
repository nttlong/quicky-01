def create_model(name,indexes,fields):
    """
    :param name:
    :param indexes:
    :param fields:
    :return:

    """
    import pymodel
    # type: (str, list(pymodel.Index), object) -> object
    return pymodel.create_model(name,indexes,fields)
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
