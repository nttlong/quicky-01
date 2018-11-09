from qmongo import models
import logging

logger = logging.getLogger(__name__)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        sorting=(lambda x: x['sorting'] if x.has_key('sorting') else None)(args['data']),
        description=(lambda x: x['description'] if x.has_key('description') else None)(args['data']),
        custom_name=(lambda x: x['custom_name'] if x.has_key('custom_name') else None)(args['data']),
        style_class=(lambda x: x['style_class'] if x.has_key('style_class') else None)(args['data']),
        url=(lambda x: x['url'] if x.has_key('url') else None)(args['data']),
        image=(lambda x: x['image'] if x.has_key('image') else None)(args['data']),
        default_name=(lambda x: x['default_name'] if x.has_key('default_name') else None)(args['data']),
        height=(lambda x: x['height'] if x.has_key('height') else None)(args['data']),
        parent_id=(lambda x: x['parent_id'] if x.has_key('parent_id') else None)(args['data']),
        active=(lambda x: x['active'] if x.has_key('active') else None)(args['data']),
        function_id=(lambda x: x['function_id'] if x.has_key('function_id') else None)(args['data']),
        type=(lambda x: x['type'] if x.has_key('type') else None)(args['data']),
        width=(lambda x: x['width'] if x.has_key('width') else None)(args['data']),
        icon=(lambda x: x['icon'] if x.has_key('icon') else None)(args['data']),
        app=(lambda x: x['app'] if x.has_key('app') else None)(args['data']),
        level_code=(lambda x: x['level_code'] if x.has_key('level_code') else None)(args['data']),
        color=(lambda x: x['color'] if x.has_key('color') else None)(args['data']),
    )

    return ret_dict

def insert(args):
    try:
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args['data'])
            idx = get_data_by_id(data['function_id'])
            if idx == 0:
                ret  =  models.SYS_FunctionList_Favorite().insert(data)
                import requests
                import json
                r = requests.post("http://localhost:3000/getDataSysFuncFavarite",
                                  headers={'Content-type': 'application/json'},
                                  data=json.dumps({'function_id': data['function_id']}))
                return ret
            else:
                return dict()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def delete(args):
    try:
        ret = {}
        if args['data'] != None:
            ret = models.SYS_FunctionList_Favorite().delete("function_id in {0}", [x["function_id"] for x in [args['data']['data']]])
            import requests
            import json
            r = requests.post("http://localhost:3000/UnPinFuncFavorite",
                              headers={'Content-type': 'application/json'},
                              data=json.dumps({'function_id': args['data']['data']['function_id']}))
            return ret
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def get_data_by_id(id):
    try:
        items = models.SYS_FunctionList_Favorite().aggregate()
        items.match("function_id == {0}", id)
        items.project(
            function_id=1
        )
        return  len(items.get_list())
    except Exception as ex:
        raise (ex)
