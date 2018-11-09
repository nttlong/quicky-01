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
    ret = qmongo.models.LMS_SurQuestionBank.aggregate
    if where.has_key("category_id") and where["category_id"] != None:
        if( isinstance(where["category_id"], unicode) ):
            ret.match("category_id == {0}", where["category_id"])
        else:
            ret.match("category_id in {0}", where["category_id"])

    ret.left_join(qmongo.models.LMS_SurQuestionCategory, "category_id", "category_id", "ca")
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.left_join(qmongo.views.SYS_VW_ValueList, "category_type", "value", "val")
    ret.match("val.list_name == {0}", "LMS_LSurQuestionType")
    ret.lookup(qmongo.models.LMS_SurveyTemplate, "question_id", "question_list", "q_list")

    if (searchText != None):
        ret.match("contains(question_id, @name) or contains(question_content_1, @name) " + \
                    "or contains(category_type_name, @name) or contains(point_scale_type, @name) " + \
                    "or contains(created_on, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)
    ret.project(
        question_id = 1,
        category_id = 1,
        question_content_1 = 1,
        question_content_2 = 1,
        question_description = 1,
        category_id_name = "ca.category_name",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        question_options=1,
        question_other_field=1,
        question_random_options=1,
        question_require_answer=1,
        question_note=1,
        active=1,
        category_type=1,
        category_type_name="val.caption",
        total_temp_size="size(q_list)"
    )
    data = ret.get_page(pageIndex, pageSize)
    return data

def insert_sur_question_bank(data):
    result = models.LMS_SurQuestionBank().insert(data)
    return result

def update_sur_question_bank(data):
    code = data['question_id']
    del data['question_id']
    result = models.LMS_SurQuestionBank().update(
        data,
        "question_id == {0}",
        code
    )

    return result

def delete_sur_question_bank(data):
    result = models.LMS_SurQuestionBank().delete(
        "question_id in @id",
        id = [x['question_id'] for x in data]
    )

    return result

def get_list_value_and_caption(data):
    result = models.LMS_SurQuestionBank().aggregate()\
    .project(
        _id = 0,
        category_id = 1,
        category_name = 1
    ).get_list()

    return result