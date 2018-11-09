from bson import ObjectId
from .. import models
import logging
import threading
from .. import common
from ..views.views import SYS_VW_ValueList
def get_list(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    #value_list = models.extend.SYS_VW_ValueList()
    value_list = SYS_VW_ValueList()
    qr = common.get_collection('LMS_SurQuestionCategory').aggregate([
        {"$lookup": {
            "from": common.get_collection_name_with_schema('SYS_VW_ValueList'),
            "localField": "category_group",
            "foreignField": "value",
            "as": "val",
        }},
        {"$unwind": {
            "path": "$val",
            "preserveNullAndEmptyArrays": False
        }},
        {"$lookup": {
            "from": common.get_collection_name_with_schema('auth_user_info'),
            "localField": "created_by",
            "foreignField": "username",
            "as": "uc",
        }},
        {"$unwind": {
            "path": "$uc",
            "preserveNullAndEmptyArrays": False
        }},
        {"$lookup": {
            "from": common.get_collection_name_with_schema('auth_user_info'),
            "localField": "modified_by",
            "foreignField": "username",
            "as": "um",
        }},
        {"$unwind": {
            "path": "$um",
            "preserveNullAndEmptyArrays": True
        }},
        {'$match': {
            '$and': [
                {'val.list_name': 'LLMS_QuestGroupType'},
                {'val.language': common.get_language()}]
        }},
        {"$lookup": {
            "from": common.get_collection_name_with_schema("LMS_SurQuestionBank"),
            "localField": "category_id",
            "foreignField": "category_id",
            "as": "sqb",
        }},
        {"$unwind": {
            "path": "$sqb",
            "preserveNullAndEmptyArrays": True
        }},
        {"$group": {
            "_id": {"category_id": "$category_id"},
            "count": {"$sum":
                          {"$max":
                               {"$cond":
                                    {"if": {"$ne": [{"$max": "$sqb.category_id"}, None]},
                                     "then": 1,
                                     "else": 0}
                                }
                           }},
            "category_id": {"$max": "$category_id"},
            "category_name": {"$max": "$category_name"},
            "category_name2": {"$max": "$category_name2"},
            "question_group": {"$max": "$category_group"},
            "question_group_display": {"$max": "$val.caption"},
            "created_on": {"$max": "$created_on"},
            "ordinal": {"$max": "$ordinal"},
            "active": {"$max": "$active"},
            "note": {"$max": "$note"},
            "created_by": {"$max":
                               {"$cond":
                                    {"if": {"$ne": ["$uc.login_account", None]},
                                     "then": {"$max": "$uc.login_account"},
                                     "else": ""}
                                }
                           },
            "modified_on": {"$max":
                                {"$cond":
                                     {"if": {"$ne": ["$modified_on", None]},
                                      "then": "$modified_on",
                                      "else": None}
                                 }
                            },
            "modified_by": {"$max":
                                {"$cond":
                                     {"if": {"$ne": ["$modified_by", None]},
                                      "then": "$um.login_account",
                                      "else": ""}
                                 }
                            }
        }},
        {"$project": {
            "_id": 0,
            "category_id": "$category_id",
            "category_name": "$category_name",
            "category_name2": "$category_name2",
            "category_group": "$question_group",
            "question_group_display": "$question_group_display",
            "num_of_questions": "$count",
            "created_on": "$created_on",
            "ordinal": "$ordinal",
            "active": "$active",
            "note": "$note",
            "modified_on": "$modified_on",
            "modified_by": "$modified_by",
            "created_by": "$created_by"
        }},
        {"$sort": common.aggregate_sort(sort)},
        {
            "$facet": {
                "metadata": [{"$count": "total"}, {"$addFields": {"page_index": pageIndex, "page_size": pageSize}}],
                "data": [{"$skip": pageSize * pageIndex}, {"$limit": pageSize}]
            }
        },
        {
            "$unwind": {"path": '$metadata', "preserveNullAndEmptyArrays": False}
        },
        {
            "$project": {
                'page_size': '$metadata.page_size',
                'page_index': '$metadata.page_index',
                'total_items': '$metadata.total',
                'items': '$data'
            }
        }
    ])

    result = list(qr)

    return (lambda x: x[0] if len(x) > 0 else {
        'page_size': pageSize,
        'page_index': pageIndex,
        'total_items': 0,
        'items': []
    })(result)

def insert_sur_question_category(data):
    result = models.LMS_SurQuestionCategory().insert(data)
    return result

def update_sur_question_category(data):
    code = data['category_id']
    del data['category_id']
    result = models.LMS_SurQuestionCategory().update(
        data,
        "category_id == {0}",
        code
    )

    return result

def delete_sur_question_category(data):
    result = models.LMS_SurQuestionCategory().delete(
        "category_id in @id",
        id = [x['category_id'] for x in data]
    )

    return result

def get_list_value_and_caption(data):
    result = models.LMS_SurQuestionCategory().aggregate()\
    .project(
        _id = 0,
        category_id = 1,
        category_name = 1
    ).get_list()

    return result