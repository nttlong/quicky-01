# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
_hasCreated=False
"""
        #is_fix: Hệ số cố định
        #coeff: #Thiết lập theo
        #coeff: #Ngày bắt đầu tính thâm niên
        """
helpers.extent_model(
    "HCSLS_Acadame",
    "base",
    [["train_level_code"]],
    train_level_code=("text",True),
    train_level_name=("text"),
    range=("numeric"),
    ordinal=("numeric"),
    note=("text"),
    #train_cof=("numeric"),
    is_fix=("numeric"),
    coeff=("numeric"),
    begin_date_cal=("numeric"),
    lock=("bool"),
    train_level_name2=("text"),
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
def HCSLS_Acadame():
        # _hasCreated=True
        # #def on_before_insert(data):
        # #    before_process
        #
        # #def on_before_update(data):
        # #    before_process(data)
        #
        # #def before_process(data):
        # #    data.update({
        # #        "detail": [{
        # #                "department_code":x['_id'],
        # #                } for x in data.get('detail',[])]
        # #        })
        #
        # #helpers.events("HCSLS_Acadame").on_before_insert(on_before_insert).on_before_update(on_before_update)
    ret = db_context.collection("HCSLS_Acadame")
    return ret