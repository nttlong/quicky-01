def create_model(name,indexes,fields):
    # type: (str, list, object) -> object
    import pymodel
    return pymodel.create_model(name,indexes,fields)
def query(*args,**kwargs):
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
