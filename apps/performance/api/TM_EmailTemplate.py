# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import common
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
from hcs_authorization import action_type,authorization
from views.views import SYS_VW_ValueList
@authorization.authorise(action=action_type.Action.READ)
def get_list(args):
    return get_email_template().get_list()

def get_email_template():
    collection = qmongo.models.TM_EmailTemplate.aggregate
    collection.lookup(SYS_VW_ValueList(), "module_name", "value", "val")
    collection.unwind("val")
    collection.match("val.language == {0}", common.get_language())
    collection.project(
        rec_id="rec_id",
        email_template_code="email_template_code",
        email_template_name="email_template_name",
        description="description",
        subject="subject",
        body="body",
        module_name="module_name",
        display_module_name="val.caption"
    )

    return collection

@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.TM_EmailTemplate.insert(args['data'])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = args['data'].copy()
            del data['email_template_code']
            del data['rec_id']
            ret  =  qmongo.models.TM_EmailTemplate.update(
                data,
                "rec_id == {0}",
                args['data']['rec_id'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = get_email_template().match("email_template_code == {0}", args['data']['email_template_code']).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.TM_EmailTemplate.delete(
                "rec_id == {0}",
                args['data']['rec_id'])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)
