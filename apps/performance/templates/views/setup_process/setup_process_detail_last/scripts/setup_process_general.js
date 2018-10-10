(function (scope) {
    var _default = {
        process_id: null,
        process_name: null,
        is_not_apply_process: false,
        max_approve_level: 0,
        is_approve_by_dept: false,
        is_require_reason: false,
        is_require_when_approve: false,
        is_require_when_reject: false,
        is_show_list_approver: false,
        is_reselect_approver: false,
        is_require_attach_file: false,
        file_size_limit: null,
        exclude_file_types: null,
        is_email_cancel: false,
        is_email_delete: false,
        is_email_instead: false,
        email_send_code: null,
        email_send_to: null,
        email_send_cc: null,
        email_send_more: null,
        email_cancel_code: null,
        email_cancel_to: null,
        email_cancel_cc: null,
        email_cancel_more: null,
        email_delete_code: null,
        email_delete_to: null,
        email_delete_cc: null,
        email_delete_more: null,
        email_instead_code: null,
        email_instead_to: null,
        email_instead_cc: null,
        email_instead_more: null,
        is_send_email_pronto: false,
        is_send_email_once: false,
        send_email_once_from_hour: null,
        send_email_once_to_hour: null,
        process_level_apply_for: null,
        score_by: null,
        score_by_coeff: null
    }
    scope._disableControl = false;

    scope.changeActive = function(event){
        $('.hcs-tab-info').find('.active').removeClass('active');
        $(event.target).closest('div').addClass('active');
    }
    scope.$parent.$parent.$parent.onSave = onSave;
    scope.$parent.$parent.$parent.onSearch = null;
    scope.$parent.$parent.$parent.onAdd = null;
    scope.$parent.$parent.$parent.onEdit = null;
    scope.$parent.$parent.$parent.onImport = null;
    scope.$parent.$parent.$parent.onExport = null;
    scope.$parent.$parent.$parent.onRefresh = null;
    scope.$parent.$parent.$parent.onDelete = null;
    scope.__mode = scope.$parent.$parent.$parent.$parent.mode;
    scope.entity = {};
    scope.$$process_id = scope.__mode == 2 ? scope.$parent.$parent.$parent.$parent.$$process_id : null;
    scope.$$curr_max_approve_level = scope.__mode == 2 ? JSON.parse(JSON.stringify(scope.$parent.$parent.$parent.$parent.$$curr_max_approve_level)) : 0;

    function onSave() {
        if(scope.entity.max_approve_level <= 0){
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('process_fail','Số cấp duyệt phải > 0')}", function () { });
            return;
        }
        if (scope.$$curr_max_approve_level < scope.entity.max_approve_level) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_res('max_approve_level_increate','Bạn đã chọn tăng số cấp duyệt tối đa. Hệ thống sẽ tự động cập nhật cấp duyệt.')}", function () {
                continuteSave(function () {
                    callApi("${get_api_key('app_main.api.TM_SetupProcess/generate_list_approve_by_max_approve_level')}",
                        {
                            "process_id": scope.__mode == 2 ? scope.$$process_id : scope.entity.process_id,
                            "max_approve_level": scope.$$curr_max_approve_level
                        }, function () {
                            scope.$parent.$parent.$parent.$parent.$$curr_max_approve_level = scope.$$curr_max_approve_level;
                        })
                });
            })
        }
        else if (scope.$$curr_max_approve_level > scope.entity.max_approve_level) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_res('max_approve_level_decreate','Bạn đã chọn giảm số cấp duyệt tối đa. Các cấp duyệt đã thiết lập vượt quá giá trị này sẽ bị xóa.')}", function () {
                continuteSave(function () {
                    callApi("${get_api_key('app_main.api.TM_SetupProcess/generate_list_approve_by_max_approve_level')}",
                        {
                            "process_id": scope.__mode == 2 ? scope.$$process_id : scope.entity.process_id,
                            "max_approve_level": scope.$$curr_max_approve_level
                        }, function () {
                            scope.$parent.$parent.$parent.$parent.$$curr_max_approve_level = scope.$$curr_max_approve_level;
                        })
                });
            })
        }
        else {
            continuteSave();
        }

        function continuteSave(fnCallBack) {
            var url = scope.__mode === 1 ? "${get_api_key('app_main.api.TM_SetupProcess/insert')}"
                : "${get_api_key('app_main.api.TM_SetupProcess/update')}";
            callApi(url, scope.entity, function (res) {
                scope.$$curr_max_approve_level = JSON.parse(JSON.stringify(scope.entity.max_approve_level));
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.$parent.$parent.$parent.$parent.$$is_approve_by_dept = scope.entity.is_approve_by_dept;
                    scope.$parent.$parent.$parent._reloadData();
                    if (fnCallBack) {
                        fnCallBack();
                    }
                }
                //else if (res.error.hasOwnProperty('code') && res.error.code == "duplicate") {
                //    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${ get_res('department_code', 'Mã phòng ban') }" + "${get_global_res('exists','đã tồn tại')}", function () { });
                //} else if (res.error.hasOwnProperty('code') && res.error.code == "missing") {
                //    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('missing_fields','Nhập liệu thiếu')}" + "\n" + 
                //        "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                //}
                else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            })
        }
    }

    /**
     * Hàm gọi api
     * @param {string} url
     * @param {object} parameter
     * @param {void} callback
     */
    function callApi(url, parameter, callback) {
        console.log(parameter)
        services.api(url)
            .data(parameter)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function _getProcessByProcessID(ProcessID, callback) {
        callApi("${get_api_key('app_main.api.TM_SetupProcess/get_list_with_process_id')}",
            {
                "process_id": ProcessID
            }, callback)
    }

    function _getDataInitCombobox() {
        //valuelist
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                    "LMS_SenderValue",
                    "LSendEmail",
                    "LPERF_ProcessLevelApplyFor"
                ]
            })
            .done()
            .then(function (res) {
//                scope.cbbSenderValue = getValue(res.values, "LMS_SenderValue");
                scope.cbbLSendEmailTo = getValue(res.values, "LSendEmail");
                scope.cbbLSendEmailCC = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailDeleteTo = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailDeleteCC = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailCancelTo = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailCancelCC = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailInsteadTo = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.cbbLEmailInsteadCC = JSON.parse(JSON.stringify(scope.cbbLSendEmailTo));
                scope.LPERF_ProcessLevelApplyFor = getValue(res.values, "LPERF_ProcessLevelApplyFor");
                scope.entity.process_level_apply_for = scope.entity.process_level_apply_for ? scope.entity.process_level_apply_for : 1;

                scope.cbbSYS_InputType = getValue(res.values, "SYS_InputType");
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
        scope.$root.$getInitComboboxData(scope,
            [
                {
                    "key": "${encryptor.get_key('cbb_nation')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('nation_code')
                        ? scope.entity.nation_code
                        : null,
                    "alias": "$$$cbb_nation"
                },
                {
                    "key": "${encryptor.get_key('cbb_province_of_nation')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('province_code')
                        ? scope.entity.province_code
                        : null,
                    "alias": "$$$province_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_district_of_province')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('district_code')
                        ? scope.entity.district_code
                        : null,
                    "alias": "$$$district_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_region')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('region_code')
                        ? scope.entity.region_code
                        : null,
                    "alias": "$$$region_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_departments')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('parent_code')
                        ? scope.entity.parent_code
                        : null,
                    "alias": "$$$cbb_departments"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('manager_code')
                        ? scope.entity.manager_code
                        : null,
                    "alias": "$$$manager_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('secretary_code')
                        ? scope.entity.secretary_code
                        : null,
                    "alias": "$$$secretary_code"
                },
                {
                    "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                    "code": scope.entity
                        && scope.entity.hasOwnProperty('signed_by')
                        ? scope.entity.signed_by
                        : null,
                    "alias": "$$$signed_by"
                }
            ]

        );
    };

    (function _init_() {
        if (scope.__mode == 2) {
            _getProcessByProcessID(scope.$$process_id, function (res) {
                scope.entity = res;
                scope.$applyAsync();
                _getDataInitCombobox();
            })
        } else {
            scope.entity = _default;
            scope.$applyAsync();
            _getDataInitCombobox();
        }
    })();

    scope.onChangeRadioButton = function (val) {
        console.log(val)
        if (val == 1) {
            scope.entity.is_send_email_pronto = true;
            scope.entity.is_send_email_once = false;
            scope.entity.is_send_email_once_from_hour = null;
            scope.entity.is_send_email_once_to_hour = null;
            scope._disableControl = 1;
        }
        else {
            scope.entity.is_send_email_pronto = false;
            scope.entity.is_send_email_once = true;
            scope._disableControl = 2;
        }
        scope.$applyAsync();
    }
});