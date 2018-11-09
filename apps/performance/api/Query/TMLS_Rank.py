from .. import models
from .. import common
import qmongo
def display_list_rank():
    ret=qmongo.models.TMLS_Rank.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        rank_code="rank_code",
        rank_name="rank_name",
        rank_name2="rank_name2",
        rank_content="rank_content",
        total_from="total_from",
        total_to="total_to",
        is_change_object="is_change_object",
        ordinal="ordinal",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret

def get_details(rank_code):
    col=qmongo.models.TMLS_Rank.aggregate.match("rank_code == {0}", rank_code)
    col.unwind("setup_change_object", False)
    col.join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    col.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    col.project(
        rec_id = "setup_change_object.rec_id",
        rank_code = "setup_change_object.rank_code",
        change_object = "setup_change_object.change_object",
        object_level = "setup_change_object.object_level",
        object_code = "setup_change_object.object_code",
        object_name = "setup_change_object.object_name",
        priority_no = "setup_change_object.priority_no",
        total_from = "setup_change_object.total_from",
        total_to = "setup_change_object.total_to",
        note = "setup_change_object.note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(setup_change_object.modified_on!='',setup_change_object.modified_on),'')",
        modified_by="switch(case(setup_change_object.modified_by!='',um.login_account),'')"
        )
    return col

def remove_details(args):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
                        {
                            "rank_code": args['data']['rank_code']
                        },
                        {
                            '$pull':{"setup_change_object" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
    return ret

def insert_details(args, details):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
                          { "rank_code": args['data']['rank_code'] },
                          {
                            '$push': {
                              "setup_change_object": details
                            }
                          }
                        )
    return ret

def update_details(args, details):
    collection  =  common.get_collection('TMLS_Rank')
    ret = collection.update(
        {
            "rank_code": args['data']['rank_code'],
            "setup_change_object":{
                "$elemMatch":{
                    "rec_id":args['data']['setup_change_object']["rec_id"]
                    }
                }
        },
        {
            "$set": {
                'setup_change_object.$.rank_code': details['rank_code'],
                'setup_change_object.$.change_object': details['change_object'],
                'setup_change_object.$.object_level': details['object_level'],
                'setup_change_object.$.object_code': details['object_code'],
                'setup_change_object.$.object_name': details['object_name'],
                'setup_change_object.$.priority_no': details['priority_no'],
                'setup_change_object.$.total_from': details['total_from'],
                'setup_change_object.$.total_to': details['total_to'],
                'setup_change_object.$.note': details['note'],
                'setup_change_object.$.modified_by': details['modified_by'],
                'setup_change_object.$.modified_on': details['modified_on']
                }
        })
    return ret

def getListRankCode(args):
    ret = {}
    collection = common.get_collection('TMLS_Rank').aggregate([
        {"$lookup":{'from':common.get_collection_name_with_schema('TMPER_AprPeriodEmpOut'), 'localField':'rank_code', 'foreignField':'rank_code', 'as': 'rr'}},
        {"$unwind":{'path':'$rr', "preserveNullAndEmptyArrays":True}},
        
        {"$project": {
            "rank_code": 1,
            "rank_name": 1,
            "ordinal": 1,
            "percent": "$rr.percent"
            
        }}
        ])
        
    ret = list(collection)


def getListRank(args):
    ret = {}
    collection = common.get_collection('TMLS_Rank').aggregate([
        {"$project": {
            "rank_code": 1,
            "rank_name": 1,
            "ordinal": 1
        }}
    ])

    ret = list(collection)
    return ret


