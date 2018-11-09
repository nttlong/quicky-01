# -*- coding: utf-8 -*-
import models
import quicky

def get_list(args):
    try:
        _language_code = quicky.language.get_language()

        list_name = args["data"].get("name", "")
        # Long sua lai
        import qmongo
        qr = qmongo.models.SYS_ValueList.aggregate.project(
            language=1,
            list_name=1,
            values=1,
        )

        if type(list_name) is list:
            qr.match("(language == {0}) and (list_name in {1})", _language_code, list_name)
            return {"values":qr.get_list()}
        elif type(list_name) in [str, unicode]:
            qr.match("(language == {0}) and (list_name == {1})", _language_code, list_name)
            return qr.get_item()
        return None
    except Exception as ex:
        return None