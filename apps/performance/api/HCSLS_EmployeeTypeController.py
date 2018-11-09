# -*- coding: utf-8 -*-
from hcs_authorization import action_type, authorization
from services import HCSLS_EmployeeTypeService as service

@authorization.authorise(action = action_type.Action.READ)
def get_list_with_searchtext(args):
    return service.get_list_with_searchtext(args)

@authorization.authorise(action = action_type.Action.CREATE)
def insert(args):
    return service.insert(args)

@authorization.authorise(action = action_type.Action.WRITE)
def update(args):
    return service.update(args)

@authorization.authorise(action = action_type.Action.DELETE)
def delete(args):
    return service.delete(args)