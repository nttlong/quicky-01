# -*- coding: utf-8 -*-
from hcs_authorization import authorization, action_type
from services import LMS_SurveyManagementSettingService as service

@authorization.authorise(action = action_type.Action.READ)
def get_data(args):
    return service.get_single_data(args['data'])
@authorization.authorise(action = action_type.Action.WRITE)
def update_or_insert(args):
    return service.update_or_insert_single_data(args['data'])

