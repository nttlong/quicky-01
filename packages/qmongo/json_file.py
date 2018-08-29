# -*- encoding: utf-8 -*-
# converting a unknown formatting file in utf-8
from . fx_model import __obj_model__
from . import json_parser
def export_to(obj,filename):
    import io
    import codecs
    import sys
    # sys.setdefaultencoding() does not exist, here!
    # reload(sys)  # Reload does the trick!
    # sys.setdefaultencoding('unicode')
    coll = obj
    if type(obj) is __obj_model__:
        coll =obj.coll
    print "Prepare.. export '{0}'".format(coll.get_collection_name())
    items = coll.get_list()
    txt = unicode(json_parser.to_json(items).decode('unicode-escape'))
    try:
        with io.open(filename, 'w', encoding="utf-8") as  fs:
            fs.write(txt)
            fs.close()

        print "Export '{0}' is successfull".format(coll.get_collection_name())
    except Exception as ex:
        print "Export '{0}' is error \n {1}".format(coll.get_collection_name(),ex.message)





def import_from(obj,filename):
    from . import json_parser
    from . import get_schema
    coll = obj

    if type(obj) is __obj_model__:
        coll = obj.coll
    coll_name = get_schema()+"."+coll._none_schema_name

    try:
        with open(filename,"r") as fs:
            txt =fs.read()
            data = json_parser.from_json(txt)
            db=coll.get_collection().database
            ret=db.get_collection(coll_name).insert_many(data)
            return ret
    except Exception as ex:
        print "Import '{0}' is error,\n {1}".format(coll_name,ex.message)





