# -*- coding: utf-8 -*-
from hcs_authorization import authorization, action_type
from services import LMS_SurveyTemplateService as service

@authorization.authorise(action = action_type.Action.READ)
def get_list(args):
    return service.get_list(args)

@authorization.authorise(action = action_type.Action.READ)
def get_data_tree(args):
    return service.get_data_tree(args)

@authorization.authorise(action = action_type.Action.CREATE)
def insert(args):
    return service.insert_survey_template(args['data'])

@authorization.authorise(action = action_type.Action.WRITE)
def update(args):
    return service.update_survey_template(args['data'])

@authorization.authorise(action = action_type.Action.DELETE)
def delete(args):
    return service.delete_survey_template(args['data'])

@authorization.authorise(action = action_type.Action.READ)
def get_value_list(args):
    return service.get_list_value_and_caption(args['data'])