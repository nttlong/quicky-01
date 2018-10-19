# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
from hcs_authorization import action_type, authorization
logger = logging.getLogger(__name__)

@authorization.authorise(action = action_type.Action.WRITE)
def update(args):
    try:
        if args['data'] != None:
            ret = models.HCSSYS_SystemConfig().update(
            args['data'],
            "_id==@_id",
            dict(
                _id = ObjectId(args['data']['_id'])
            ))
            from .. import SystemConfig
            SystemConfig.update()
            return ret
        return None
    except Exception as ex:
        logger.debug(ex)
        raise(ex)