from .. import common
from qmongo import qcollections
def get_all_department_by_year_month(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [{'apr_period': args['apr_period']}, {'apr_year': args['apr_year']}]
        }},
        {"$project": {
            "_id": 1,
            "apr_period": 1,
            "apr_year": 1,
            "department_code": 1,
            "rank_level": 1,
            "note": 1
        }},
    ])

    ret = list(collection)
    return ret

def get_aprAprRank_by_departCode(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [{'apr_period': args['apr_period']}, {'apr_year': args['apr_year']},
                     {'department_code': args['departments']['department_code'][0]}]
        }},
        {"$project": {
            "_id": 1,
            "apr_period": 1,
            "apr_year": 1,
            "department_code": 1,
            "rank_level": 1,
            "note": 1
        }},
    ])

    ret = list(collection)
    return (lambda x: x[0] if len(x) > 0 else None)(ret)


def get_parent_code_by_departCode(args):
    if (args != None):
        ret = []
        used = []
        qr = qcollections.queryable(common.get_collection("HCSSYS_Departments")).items
        for i in args:
            for x in qr:
                if (i == x['department_code']):
                    ret.append(x['parent_code'])
                    break
        unique = list(set(ret))
        return unique
