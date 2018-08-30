from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_Position",
            "base",
            [["job_pos_code"]],
            job_pos_code=("text",True),
            job_pos_name=("text", True),
            job_pos_name2=("text"),
            man_level=("numeric", True),
            ordinal=("numeric"),
            note=("text"),
            is_fix=("numeric"),
            coeff=("numeric"),
            begin_date_cal=("numeric"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
            details=("list",False,dict(
                rec_id = ("text"),
                seniority_from = ("numeric"),
                seniority_to = ("numeric"),
                coefficient = ("numeric"),
                salary = ("numeric"),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
            ))
        )
        #def on_before_insert(data):
        #    before_process

        #def on_before_update(data):
        #    before_process(data)

        #def before_process(data):
        #    data.update({
        #        "detail": [{
        #                "department_code":x['_id'],
        #                } for x in data.get('detail',[])]
        #        })

        #helpers.events("HCSLS_Acadame").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSLS_Position():
    ret = db_context.collection("HCSLS_Position")
    return ret