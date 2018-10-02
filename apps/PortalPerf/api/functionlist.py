from . import models
import logging
logger = logging.getLogger(__name__)
import common

def get_list(args):
    items = models.models_per.SYS_FunctionList().aggregate()
    items.left_join(models.models_per.HCSSYS_FunctionListSummary(), "function_id", "function_id", "uc")
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
        sumary               = "uc"
        ).match("app == {0}", "PortalPerf").sort({"sorting":1})
    data = items.get_list()
    for x in data:
        if x.has_key('sumary') and x['sumary'] != None:
            x['number'] = exec_query(x['sumary'])
    return data

def get_list_module(args):
    ret = models.HCSSYS_Modules().aggregate().sort({"odinal": 1})
    return ret.get_list()

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