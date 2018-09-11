# -*- coding: utf-8 -*-
import models
import quicky

def get_list(args):
    try:
        items = models.LMSSYS_Value_List().aggregate().project(
            language = 1,
            list_name = 1,
            values = 1,
            )

        _language_code = quicky.language.get_language()

        list_name = args["data"].get("name", "")

        if type(list_name) is list:
            ret = []
            for x in list_name:
                items.match("(language == @lan) and (list_name == @name)", lan=_language_code, name=x)
                ret.append(items.get_item())
            return {"values":ret}
        elif type(list_name) in [str, unicode]:
            if args["data"].has_key('name'):
                items.match("(language == @lan) and (list_name == @name)", lan=_language_code, name=list_name)
                return items.get_item()
        
        return None
    except Exception as ex:
        return None