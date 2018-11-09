from .. import models, common
import qmongo
def display_list_apr_period():
    ret=qmongo.models.TMPER_AprPeriod.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        emp_final_from="emp_final_from",
		emp_final_to="emp_final_to",
        approval_final_from="approval_final_from",
        approval_final_to="approval_final_to",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        apr_year = 1
        ))

    return ret


def get_period_by_apr_period(apr_period):
    ret=qmongo.models.TMPER_AprPeriod.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        give_target_from="give_target_from",
        give_target_to="give_target_to",
        review_mid_from="review_mid_from",
        review_mid_to="review_mid_to",
        approval_mid_from="approval_mid_from",
        approval_mid_to="approval_mid_to",
        emp_final_from="emp_final_from",
        emp_final_to="emp_final_to",
        approval_final_from="approval_final_from",
        approval_final_to="approval_final_to",
        note="note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    ret.match("apr_period == {0}",args['data']['apr_period']);
    ret.sort(dict(
        apr_year = 1
    ))

    return ret


def get_apr_rank_by_apr_period_year(apr_period, apr_year):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [ { 'apr_year': apr_year }, { 'apr_period': apr_period } ]
        }},
        {"$project": {
            "_id": 1,
        }},
    ])
    ret = list(collection)
    return ret

def update_rank_level_when_insert_rank_to_sync(rank_code,percent):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank')
    ret = collection.update_many({'rank_level':{'$ne':None}},
                {'$push':{'rank_level':{
                    'rank_code':rank_code, 'percent': percent
                }
                }
            }
        )
    return ret

def update_rank_level_when_delete_rank_to_sync(datas):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank')
    ret = collection.update_many({'rank_level':{'$ne':None}},
    {'$pull': {'rank_level':{
        'rank_code':{'$in': [d['rank_code'] for d in datas]}
    }}})
    return ret