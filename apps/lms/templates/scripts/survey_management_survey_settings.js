(function (scope) {
    debugger
    var __model__ ={
        _id:null,
        ques_order:null,
        allow_pause_resumse:false,
        allow_anony_survey:false,
        prevent_num_res:false,
        ques_nav_sur:false,
        survey_time_limit:null,
        survey_res_limit:null,
        show_process_bar:false,
        show_ques_num:false,
        allow_res_edit:false,
        notif_email_temp:null,
        notif_send_to:null,
        notif_CC:null,
        notif_BCC:null,
        notif_send_mail:null,
        notif_from_date:null,
        notif_to_date:null,
        notif_from_time:null,
        notif_to_time:null,
        survey_send_email_again:null,
        confirm_email_temp:null,
        confirm_send_to:null,
        confirm_CC:null,
        confirm_BCC:null,
        confirm_send_mail:null,
        confirm_from_date:null,
        confirm_to_date:null,
        confirm_from_time:null,
        confirm_to_time:null,
        course_evalua_students:false,
        survey_temp_students:null,
        course_evalua_teachers:false,
        survey_temp_teachers:null,
        course_evalua_dept:false,
        survey_temp_dept:null,
        supplier_evalua_dept:false,
        survey_temp_sup_dept:null,
        emp_voice:false,
        survey_temp_emp_voice:null,
        other_sur:false,
        survey_temp_other:null,
    }
    
    setTimeout(function(){
        var tabNotification = $('#tabNotification');
        var tabConfirmation = $('#tabConfirmation');
        // var _collapseNotify = collapse(tabNotification.find('.zb-content'));
        // var _collapseConfirm = collapse(tabConfirmation.find('zb-content'));

        function collapse(ele) {
            if (ele.find('.zb-content').is(":hidden")) {
                ele.find(".zb-header-icon i").addClass("zb-icon-up");
                ele.find(".zb-header-icon i").removeClass("zb-icon-down");
            } else {
                ele.find(".zb-header-icon i").removeClass("zb-icon-up");
                ele.find(".zb-header-icon i").addClass("zb-icon-down");
            }
            var toggle = ele.find('.zb-content').slideToggle(300);
        }
        $(document).ready(function(){
            tabNotification.find('.zb-header-icon i').bind("click", function(){
                collapse(tabNotification);
            });
            tabNotification.find(".zb-header-title").bind("click", function(){
                collapse(tabNotification);
            });
        })

        $(document).ready(function(){
            tabConfirmation.find('.zb-header-icon i').bind("click", function(){
                collapse(tabConfirmation);
            });
            tabConfirmation.find(".zb-header-title").bind("click", function(){
                collapse(tabConfirmation);
            });
        });
    }, 500)

     scope.dt_true = true;
    scope.dt_false= false;

    scope.changeActive = function(event){
        $('.hcs-tab-info').find('.active').removeClass('active');
        $(event.target).closest('div').addClass('active');
    }


    function getInitialData(){
    
        services.api("${get_api_key('app_main.api.LMS_SurveyManagementSetting/get_data')}")
                .data({})
                .done()
                .then(function (res) {
                    debugger
                    scope.entity = res
                    callback(res);
                })

    };

    scope.onSave = function(){
        if(scope.entity){
            debugger
            editData(function (res) {
                if (res.error == null) {

                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);

                } else {
                    $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                }
            })
           
            

        }
    }
        function editData(callback) {
            var param = _.mapObject(__model__, function(val, key) {
                return val = scope.entity[key] ? scope.entity[key] : null
            });
            services.api("${get_api_key('app_main.api.LMS_SurveyManagementSetting/update_or_insert')}")
                .data(param)
                .done()
                .then(function (res) {
                    callback(res);
                })
        }

   
    scope.reloadData = function (){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
    }

    scope.onImport = function(){
        
    }

    scope.onExport = function(){
        
    }

    scope.onRefresh = function(){
        scope.reloadData();
    }

    function init() {
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        getInitialData();
    }
    init();

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
        {
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        }else{
            window.location.href = '#page=' + scope.$root.$extension.TripleDES.encrypt(data['page']);
        }
    }); 
    function _getDataInitCombobox() {

            scope.$root.$getInitComboboxData(scope, {
                "key": "${encryptor.get_key('lms_cbb_sur_question_category')}",
                "code": scope.entity
                        && scope.entity.hasOwnProperty('category_group')
                        ? scope.entity.category_group
                        : null,
                "alias": "$$$lms_cbb_sur_question_category"
            });
            scope.$root.$getInitComboboxData(scope, {
                "key": "${encryptor.get_key('lms_cbb_sur_template')}",
                "code": scope.entity
                        && scope.entity.hasOwnProperty('category_group')
                        ? scope.entity.category_group
                        : null,
                "alias": "$$$lms_cbb_sur_template"
            });
        }
        _getDataInitCombobox();
    loadValueList();
         function loadValueList() {
            services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                     "LMS_LSurveySendEmailAgainAfter",
                    "LMS_LSurveySetResponseLimit",
                    "LMS_LSurveySetTimeLimit",
                    "LMS_LSurveyQuestionOrder",
                    
                ]
            })
            .done()
            .then(function (res) {
                scope.vll_LMS_LSurvey_send_email_again_after = getValue(res.values, "LMS_LSurveySendEmailAgainAfter");
                scope.vll_LMS_LSurvey_set_response_limit= getValue(res.values, "LMS_LSurveySetResponseLimit");
                scope.vll_LMS_LSurvey_set_time_limit = getValue(res.values, "LMS_LSurveySetTimeLimit");
                scope.vll_LMS_LSurvey_question_order = getValue(res.values, "LMS_LSurveyQuestionOrder");
                scope.entity = JSON.parse(JSON.stringify(scope.entity? scope.entity: __model__));
                scope.entity.survey_time_limit=1;
                scope.entity.survey_res_limit=1;
                scope.entity.survey_send_email_again=1;
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
        }
});