from bson import ObjectId
from .. import models
import qmongo
import logging
import threading
from .. import common
from ..views.views import SYS_VW_ValueList

from qmongo.qcollections import queryable as query





def get_single_data(args):
    qr = query(common.get_db_context(), 'lv.LMS_SurveyManagementSetting').limit(1)
    return qr.item

def update_or_insert_single_data(data):

    collection  =  common.get_collection('LMS_SurveyManagementSetting')
    if data['_id'] != None:
        code = data['_id']
        del data['_id']
        ret = collection.update(
                { "_id": ObjectId(code) },
                {
                    '$set': data
                }
            )
        return dict(
            error=None
        )
    else:
        del data['_id']
        ret = collection.insert(data)
        return  dict(
            error = None
        )

    return dict(
        error="request parameter is not exist"
    )