# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_JobWorking",
            "base",
            [["job_w_code"]],
            job_w_code = ("text", True),
            job_w_name = ("text", True),
            job_w_name2 = ("text"),
            job_w_duty = ("text"),
            gjw_code = ("text", True),
            ordinal = ("numeric"),
            lock = ("bool"),
            is_job_w_main_staff = ("bool"),
            report_to_job_w=("text"),
            internal_process = ("text"),
            combine_process = ("text"),
            description = ("text"),
            effect_date = ("date"),
            job_pos_code = ("text"),
            dept_apply = ("list"),
            dept_contact = ("list"),
            job_w_next = ("list"),
            job_w_change = ("list"),
            task = ("list",False,dict(
                rec_id = ("text"),
                task_name = ("text"),
                weight = ("numeric"),
                description = ("text"),
                ordinal = ("numeric"),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
                )),
            factor_appraisal = ("list",False,dict(
                rec_id = ("text"),
                factor_code = ("text"),
                job_w_code = ("text"),
                weight = ("numeric"),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
                )),
            kpi = ("list",False,dict(
                rec_id = ("text"),
                kpi_code = ("text"),
                kpi_name = ("text"),
                unit = ("numeric"),
                description = ("text"),
                cycle = ("numeric"),
                weight = ("numeric"),
                score_from = float,
                score_to = float,
                standard_mark = ("numeric"),
                ordinal = ("numeric"),
                note = ("text"),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
                )),
            competency = ("list",False,dict(
                rec_id = ("text"),
                grade = ("numeric"), #pk, require
                com_code = ("text"),#pk, require
                com_level_code = ("text"),#pk, require
                weight = ("numeric"),
                ordinal = ("numeric"),
                note = ("text"),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
                )),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_JobWorking():
    ret = db_context.collection("HCSLS_JobWorking")
    return ret