from .. import models
from .. import common
#from ..views.views import HCSLS_VW_JobWorkingCompetency
import datetime
def insert_job_working_competency(job_w_code, comp):
    import qmongo
    try:
        if(len(job_w_code)) > 0:
            exist = qmongo.views.HCSLS_VW_JobWorkingCompetency.aggregate.project(
                rec_id = 1,
                job_w_code = 1,
                grade = 1,
                com_code = 1,
                com_level_code = 1,
                weight = 1,
                ordinal = 1,
                note = 1,
                created_on = 1,
                created_by = 1,
                modified_on = 1,
                modified_by = 1
                ).match("com_code == @com_code", com_code = comp['com_code']).get_list()
            list_insert = []
            for x in job_w_code:
                if x not in map(lambda d: d['job_w_code'], exist):
                    list_insert.append({
                        "rec_id": common.generate_guid(),
                        "job_w_code": x,
                        "grade": comp.get("grade", None),
                        "com_code": comp.get("com_code", None),
                        "com_level_code": comp.get("com_level_code", None),
                        "weight": comp.get("weight", None),
                        "ordinal": comp.get("ordinal", None),
                        "note": comp.get("note", None),
                        "created_on": datetime.datetime.now(),
                        "created_by": common.get_user_id()
                        })
                else:
                    find = filter(lambda y: y['job_w_code'] == x, exist)[0]
                    list_insert.append(find)

            ret = {}
            for x in exist:
                ret = common.get_collection('HCSLS_JobWorking').update(
                        {
                            "job_w_code": x['job_w_code']
                        },
                        {
                            '$pull':{"competency" :{ "rec_id": x['rec_id']}}
                        },
                        True
                        )

            if len(list_insert) > 0:
                for x in list_insert:
                    code = x['job_w_code']
                    del x['job_w_code']
                    ret = common.get_collection('HCSLS_JobWorking').update(
                        { "job_w_code": code },
                        {
                        '$push': {
                            "competency": x
                            }
                        }
                        )

            return ret

    except Exception as ex:
        raise(ex)
