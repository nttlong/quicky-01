# -*- coding: utf-8 -*-
from hcs_authorization import action_type, authorization
from services import TMPER_TargetKPIService as service

@authorization.authorise(action=action_type.Action.READ)
def get_list(args):
    return service.get_list_giao(args)

@authorization.authorise(action=action_type.Action.READ)
def get(args):
    return service.get(args)

@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    return service.insert(args)

@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    return service.update(args)

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    return service.delete(args)

@authorization.authorise(action=action_type.Action.CREATE)
def generate(args):
    return service.generate(args)

@authorization.authorise(action=action_type.Action.READ)
def get_list_target(args):
    return service.get_target_kpi_by__apr_period_and_apr_year_and_emp_code(args)

@authorization.authorise(action=action_type.Action.READ)
def get_list_update_target(args):
    return service.get_list_update_target(args)

@authorization.authorise(action=action_type.Action.READ)
def get_list_update_target_by_id(args):
    return service.get_list_update_target_by_id(args)