from . import models
import logging
logger = logging.getLogger(__name__)
import common
import qmongo
def get_list(args):
    if (args["data"] == None or args["data"].has_key("language") == False or args["data"]["language"] == None):
        return dict();

    lang = args["data"]["language"]

    if (lang == "vi"):
        lang = 'vn'

    lang = lang.upper()

    items = qmongo.models.SYS_FunctionList.aggregate
    items.left_join(qmongo.models.HCSSYS_FunctionListSummary, "function_id", "function_id", "uc")
    items.left_join(qmongo.models.HCSSYS_FunctionListLabel, "function_id", "function_id", "lb")
    items.left_join(qmongo.models.SYS_FunctionList_Favorite, "function_id", "function_id", "fv")
    items.match("(lb.language == {0}) or ((image != {1}) and (image != {2}))", lang, "", None)
    items.project(
        sorting              = 1,
        description          = 1,
        custom_name          = 1,
        style_class          = 1,
        url                  = 1,
        image                = 1,
        default_name         = 1,
        height               = 1,
        parent_id            = 1,
        active               = 1,
        function_id          = 1,
        type                 = 1,
        width                = 1,
        icon                 = 1,
        app                  = 1,
        level_code           = 1,
        color                = 1,
        sumary               = "uc",
        default_name_lb      = "lb.default_name",
        custom_name_lb       = "lb.custom_name",
        description_lb       = "lb.description",
        favorites            = "fv.function_id"
        ).match("app == {0}", "PortalLms").sort({"sorting":1})
    data = items.get_list()
    for x in data:
        if x.has_key('sumary') and x['sumary'] != None:
            x['number'] = exec_query(x['sumary'])
    return data

def get_list_module(args):
    if(args["data"] == None or args["data"].has_key("language") == False or args["data"]["language"] == None):
        return dict();

    lang = args["data"]["language"]

    if (lang == "vi"):
        lang = 'vn'

    lang = lang.upper()

    collection = common.get_collection('HCSSYS_Modules')

    ret = collection.aggregate([
        {
            "$sort": {"sorting": 1}
        }, {
            "$match": {
                "module_type": "portal"
            }
        }, {
        "$lookup":
           {
                "from": common.get_collection_name_with_schema('HCSSYS_FunctionListLabel'),
                "let": { "module_code": "$module_code" },
                "pipeline": [
                    { "$match":
                        { "$expr":
                            {
                                "$and": [
                                    {
                                        "$eq": ["$language", lang]
                                    }, {
                                        "$eq": [ "$function_id",  "$$module_code" ]
                                    }, {
                                        "$eq": ["$application", "HCSSYS_Modules"]
                                    }
                                ]
                            }
                        }
                    },
                    { "$project": { "function_id": 1, "language": 1, "default_name": 1, "custom_name": 1, "description": 1 } }
                ],
                "as": "stockdata"
            }
        }, {
            "$unwind": "$stockdata"
        }, {
            "$project": {
                "module_code": 1,
                "module_name": 1,
                "module_type": 1,
                "url":         1,
                "redirect_url": 1,
                "is_active":   1,
                "sorting": 1,
                "is_new_tab": 1,
                "default_name": "$stockdata.default_name",
                "custom_name": "$stockdata.custom_name",
                "description": "$stockdata.description",
                "function_id": "$stockdata.function_id",
            }
        }

    ])

    #ret = models.HCSSYS_Modules().aggregate()
    #ret.match("module_type == {0}", "portal")
    #ret.sort({"sorting": 1})
    #ret.left_join()
    #ret.project(
    #    module_code = 1,
    #    module_name = 1,
    #    module_type = 1,
    #    url = 1,
    #    redirect_url = 1,
    #    is_active = 1,
    #    sorting = 1,
    #    is_new_tab = 1,
    #    lb = 1
    #)
    return list(ret)

def exec_query(args):
    import json
    try:
        tab = args['collection']
        query = args['query']
        col = common.get_collection(tab)
        result = list(col.aggregate(json.loads(query)))
        if result != None and len(result) > 0:
            return result[0]['number']
        return None
    except Exception as ex:
        logger.debug(ex)
        return {"data": None, "error": ex.message}

def get_tree(args):
    items = models.models_per.SYS_FunctionList().aggregate().project(
        function_id      = 1,
        parent_id        = 1,
        default_name     = 1,
        app              = 1
        ).match("app == {0}", "PERF")
    
    return items.get_list()