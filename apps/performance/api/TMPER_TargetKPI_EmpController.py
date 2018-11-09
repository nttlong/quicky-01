# -*- coding: utf-8 -*-
from hcs_authorization import action_type, authorization
from services import TMPER_TargetKPI_EmpService as service

@authorization.authorise(action=action_type.Action.READ)
def get_list(args):
    return service.get_list_giao(args)

@authorization.authorise(action=action_type.Action.READ)
def get_list_employee_in_apr_period(args):
    return service.get_list_employee_in_apr_period(args)

@authorization.authorise(action=action_type.Action.READ)
def count_employee(args):
    return service.count_employee_with_status_give_target(args)