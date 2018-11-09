# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import qmongo
from models.SYS_ValueList import SYS_ValueList
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=qmongo.models.LMSLS_ExExamination.aggregate
    ret.lookup(qmongo.views.SYS_VW_ValueList, "course_related", "value", "val")
    ret.unwind("val", False)
    ret.match("val.list_name == {0}", "LMS_Ex_ExamType")
    ret.project(
            exam_id=1,
            exam_name1=1,
            exam_category=1,
            course_related=1,
            question_list=1,
            exam_avail=1,
            duration=1,
            exam_mode=1,
            specific_avail=1,
            status=1,
            course_related_name="val.caption",
            retake_time_list=1
        )
  
    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    return  data

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None: 
            data =  set_dict_insert_data(args)
            ret  =  qmongo.models.LMSLS_ExExamination.insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  qmongo.models.LMSLS_ExExamination.update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item=qmongo.models.LMSLS_ExExamination.aggregate.match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.LMSLS_ExExamination.delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete_one(id):
    try:
        lock.acquire()
        ret = {}
        if id['data'] != '':
            ret  =  qmongo.models.LMSLS_ExExamination.delete("_id == {0}", ObjectId(id['data']))
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        exam_id= (lambda x: x['exam_id'] if x.has_key('exam_id') else None)(args['data']),
        exam_name1= (lambda x: x['exam_name1'] if x.has_key('exam_name1') else None)(args['data']),
        exam_name2= (lambda x: x['exam_name2'] if x.has_key('exam_name2') else None)(args['data']),
        course_related= (lambda x: x['course_related'] if x.has_key('course_related') else None)(args['data']),
        course_info= (lambda x: x['course_info'] if x.has_key('course_info') else None)(args['data']),
        exam_avail= (lambda x: x['exam_avail'] if x.has_key('exam_avail') else None)(args['data']),
        exam_mode= (lambda x: x['exam_mode'] if x.has_key('exam_mode') else None)(args['data']),
        exam_form= (lambda x: x['exam_form'] if x.has_key('exam_form') else None)(args['data']),
        who_take_exam= (lambda x: x['who_take_exam'] if x.has_key('who_take_exam') else [])(args['data']),
        assign_candidate= (lambda x: x['assign_candidate'] if x.has_key('assign_candidate') else None)(args['data']),
        choose_from= (lambda x: x['choose_from'] if x.has_key('choose_from') else None)(args['data']),
        mode_pick= (lambda x: x['mode_pick'] if x.has_key('mode_pick') else None)(args['data']),
        question_category= (lambda x: x['question_category'] if x.has_key('question_category') else [])(args['data']),
        exam_category= (lambda x: x['exam_category'] if x.has_key('exam_category') else None)(args['data']),
        exam_temp_name1= (lambda x: x['exam_temp_name1'] if x.has_key('exam_temp_name1') else None)(args['data']),
        question_list= (lambda x: x['question_list'] if x.has_key('question_list') else [])(args['data']),
        retake_exam= (lambda x: x['retake_exam'] if x.has_key('retake_exam') else None)(args['data']),
        retake_all= (lambda x: x['retake_all'] if x.has_key('retake_all') else None)(args['data']),
        retake_condition= (lambda x: x['retake_condition'] if x.has_key('retake_condition') else None)(args['data']),
        result_less= (lambda x: x['result_less'] if x.has_key('result_less') else None)(args['data']),
        retake_time= (lambda x: x['retake_time'] if x.has_key('retake_time') else None)(args['data']),
        different_time=(lambda x: x['different_time'] if x.has_key('different_time') else None)(args['data']),
        list_time_retake= (lambda x: x['list_time_retake'] if x.has_key('list_time_retake') else [])(args['data']),
        range_time= (lambda x: x['range_time'] if x.has_key('range_time') else None)(args['data']),
        scoring_method= (lambda x: x['scoring_method'] if x.has_key('scoring_method') else None)(args['data']),
        show_result= (lambda x: x['show_result'] if x.has_key('show_result') else None)(args['data']),
        customize= (lambda x: x['customize'] if x.has_key('customize') else None)(args['data']),
        minium_score= (lambda x: x['minium_score'] if x.has_key('minium_score') else None)(args['data']),
        add_feedback= (lambda x: x['add_feedback'] if x.has_key('add_feedback') else None)(args['data']),
        result_type= (lambda x: x['result_type'] if x.has_key('result_type') else None)(args['data']),
        assign_exam= (lambda x: x['assign_exam'] if x.has_key('assign_exam') else None)(args['data']),
        minimum_score= (lambda x: x['minimum_score'] if x.has_key('minimum_score') else None)(args['data']),
        certificate= (lambda x: x['certificate'] if x.has_key('certificate') else None)(args['data']),
        display_result= (lambda x: x['display_result'] if x.has_key('display_result') else None)(args['data']),
        ques_order= (lambda x: x['ques_order'] if x.has_key('ques_order') else None)(args['data']),
        ques_navi= (lambda x: x['ques_navi'] if x.has_key('ques_navi') else None)(args['data']),
        allow_candidates= (lambda x: x['allow_candidates'] if x.has_key('allow_candidates') else None)(args['data']),
        preview_time= (lambda x: x['preview_time'] if x.has_key('preview_time') else None)(args['data']),
        text_high= (lambda x: x['text_high'] if x.has_key('text_high') else None)(args['data']),
        ques_dis= (lambda x: x['ques_dis'] if x.has_key('ques_dis') else None)(args['data']),
        result_SMS= (lambda x: x['result_SMS'] if x.has_key('result_SMS') else None)(args['data']),
        result_email= (lambda x: x['result_email'] if x.has_key('result_email') else None)(args['data']),
        pause_resume= (lambda x: x['pause_resume'] if x.has_key('pause_resume') else None)(args['data']),
        check_plagi= (lambda x: x['check_plagi'] if x.has_key('check_plagi') else None)(args['data']),
        show_hint= (lambda x: x['show_hint'] if x.has_key('show_hint') else None)(args['data']),
        duration= (lambda x: x['duration'] if x.has_key('duration') else None)(args['data']),
        edit_instruction=(lambda x: x['edit_instruction'] if x.has_key('edit_instruction') else None)(args['data']),
        specific_avail= (lambda x: x['specific_avail'] if x.has_key('specific_avail') else None)(args['data']),
        status= (lambda x: x['status'] if x.has_key('status') else None)(args['data']),
        disable= (lambda x: x['disable'] if x.has_key('disable') else None)(args['data']),
        note=(lambda x: x['note'] if x.has_key('note') else None)(args['data']),
        certificate_template=(lambda x: x['certificate_template'] if x.has_key('certificate_template') else None)(args['data']),
        retake_time_list=(lambda x: x['retake_time_list'] if x.has_key('retake_time_list') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['exam_id']
    return ret_dict
#def get_level_code_by_folder_id(args):
#    where = args['data'].get('where')
#    ret=models.LMSLS_ExExamination().aggregate()
#    if(where != None):
#        ret.match("(folder_id==@folder_id)",folder_id=where['folder_id'])
#    ret.project(
#        level_code=1
#        )
#    return ret.get_page(0, 100)

def get_data_examination_by_id(args):
    try:
        ret = {}
        if args['data'] != None:
            where = args['data']
            ret  =  qmongo.models.LMSLS_ExExamination.aggregate
            ret.project(
                    exam_id=1,
                    exam_name1=1,
                    exam_name2=1,
                    exam_form=1,
                    exam_mode=1,    
                    course_related=1,
                    course_info=1,
                    duration=1,
                    show_result=1,
                    exam_avail=1,
                    display_result=1,
                    #negavtive_mark=1,
                    minimum_score=1,
                    result_type=1,
                    mode_pick=1,
                    ques_order=1,
                    text_high=1,
                    ques_dis=1,
                    ques_navi=1,
                    certificate=1,
                    retake_exam=1,
                    retake_condition=1,
                    retake_all=1,
                    result_less=1,
                    allow_candidates=1,
                    show_hint=1,
                    result_email=1,
                    result_SMS=1,
                    pause_resume=1,
                    check_plagi=1,
                    exam_total_ques=("size(question_list)"),
                    specific_avail=1,
                    assign_candidate=1,
                    choose_from=1,
                    exam_category=1,
                    exam_temp_name1=1,
                    retake_time=1,
                    different_time=1,
                    range_time=1,
                    scoring_method=1,
                    customize=1,
                    minium_score=1,
                    assign_exam=1,
                    preview_time=1,
                    add_feedback=1,
                    list_time_retake=1,
                    edit_instruction=1,
                    status=1,
                    disable=1,
                    note=1,
                    certificate_template=1,
                )
            # test
            if(where.has_key('exam_id')):
                ret.match("(exam_id==@exam_id)",exam_id=where['exam_id'])
            return ret.get_item()

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)


def get_data_table_examination_by_id(args):
    try:
        ret = {}
        if args['data'] != None:
            pageSize = args['data'].get('pageSize', 0)
            pageIndex = args['data'].get('pageIndex', 20)
            sort = args['data'].get('sort', 20)
            where = args['data']
            pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
            ret  =  qmongo.models.LMSLS_ExExamination.aggregate

            if(where.has_key('exam_id')):
                ret.match("(exam_id==@exam_id)",exam_id=where['exam_id'])

            ret.unwind("question_list")
            ret.replace_root("question_list")
            ret.left_join( qmongo.models.LMSLS_ExQuestionCategory, "ques_category", "category_id", "category")
            dataRet = ret.get_page(pageIndex, pageSize)
            # data valuelist map qua dataRet
            dataValueList = []
            dataValuelistType = get_data_valuelist('LMSEx_ques_type')
            dataValuelistLevel = get_data_valuelist('LMSEx_ques_level')
            dataValueList.append(
                dict(
                    localField="ques_type",
                    fieldName="ques_type_name",
                    dataVal=dataValuelistType
                    )
                )
            dataValueList.append(
                dict(
                    localField="ques_level",
                    fieldName="ques_level_name",
                    dataVal=dataValuelistLevel
                    )
                )
            #
            dataRet['items'] = lookup_list_data_value_list(dataRet['items'], dataValueList)
            return dataRet

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def get_data_valuelist (val):
    try:
        if val != None:
            import quicky
            _language_code = quicky.language.get_language()
            ret = qmongo.models.SYS_ValueList.aggregate.match("(language == @lan) and (list_name == @name)", lan=_language_code, name=val)
            ret.unwind("values")
            ret.replace_root("values")
            #ret.project(
            #    language = 1,
            #    list_name = 1,
            #    values = 1,
            #    )
            return ret.get_list()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def lookup_list_data_value_list(list1, list2):
    if(list1 != None and list2 != None and len(list1) > 0 and len(list2) > 0):
        i = 0
        for item in list1:
            i+=1
            item['stt'] = i
            for item2 in list2:
                data_list = [x for x in item2['dataVal'] if x['value'] == item[item2['localField']]]
                if(data_list != None and len(data_list) > 0):
                    item[item2['fieldName']] = data_list[0]['caption']
        return list1

def get_exam_retake_list(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=qmongo.models.LMSLS_ExExamination.aggregate
    ret.project(
            exam_id=1, 
            exam_name1=1,
            course_related=1,
            result_less=1,
            list_time_retake=1,
            retake_condition=1,
            retake_time=1,
            retake_exam=1,
            range_time=1,
        )
  
    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    data['items'] = getDataRetake(data['items'])

    return  data

def getDataRetake (item):
    import datetime
    if (item != None) and (len(item) > 0):
        for x in item:
            if x.has_key('retake_time') and x['retake_time'] != None and x['retake_time'] == True:
                if x.has_key('list_time_retake') and x['list_time_retake'] != None and len(x['list_time_retake']) > 0:
                    ilength = len(x['list_time_retake'])
                    dt = x['list_time_retake']
                    x['start_date'] = dt[0]['start_date']#.strftime("%d.%m.%Y")
                    x['end_date'] = dt[ilength - 1]['end_date']#.strftime("%d.%m.%Y")
            else:
                if x.has_key('range_time') and x['range_time'] != None:
                    dt = x['range_time']
                    x['start_date'] = dt['start_date']#.strftime("%d.%m.%Y")
                    x['end_date'] = dt['end_date']#.strftime("%d.%m.%Y")
        return item
    return item