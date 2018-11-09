from bson import ObjectId
from .. import models
import logging
import threading
from .. import common
from ..views.views import SYS_VW_ValueList
import qmongo
def get_list(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = qmongo.models.LMS_SurveyTemplate.aggregate
    if where.has_key("survey_type") and where["survey_type"] != None:
        ret.match("survey_type == {0}", where["survey_type"])

    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.left_join(qmongo.views.SYS_VW_ValueList, "survey_type", "value", "val")
    ret.match("val.list_name == {0}", "LMS_LSurveyType")

    if (sort != None):
        ret.sort(sort)
    ret.project(
        survey_id = 1,
        survey_type = 1,
        temp_survey_1 = 1,
        temp_survey_2 = 1,
        order = 1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        active=1,
        question_list=1,
        survey_type_name="val.caption"
    )
    data = ret.get_page(pageIndex, pageSize)
    return data

def insert_survey_template(data):
    result = qmongo.models.LMS_SurveyTemplate.insert(data)
    return result

def update_survey_template(data):
    code = data['survey_id']
    del data['survey_id']
    result = qmongo.models.LMS_SurveyTemplate.update(
        data,
        "survey_id == {0}",
        code
    )

    return result

def delete_survey_template(data):
    result = qmongo.models.LMS_SurveyTemplate.delete(
        "survey_id in @id",
        id = [x['survey_id'] for x in data]
    )

    return result

def get_list_value_and_caption(data):
    result =qmongo.models.LMS_SurveyTemplate.aggregate()\
    .project(
        _id = 0,
        survey_id = 1,
        temp_survey_1 = 1
    ).get_list()

    return result