﻿(function (scope) {
    scope.__mode = 0;
    scope.entity = {};
    //scope.$active = (scope.$root.$commons) ? scope.$root.$commons.$active : true
    console.log("dô nè active", scope.$active)
    scope.$parent.$parent.$parent.onSave = (scope.$active) ? onSave : "";
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onPrint = onPrint;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;

    scope.changeActive = function(event){
        $('.hcs-tab-info').find('.active').removeClass('active');
        $(event.target).closest('div').addClass('active');
    }

    scope.set_job_w_code = function () {
        var frm = lv.FormSearch(scope, "$$$job_working");
        frm.JobWorking(scope.entity, "job_w_code", "${get_res('job_w_code','Chức danh')}", false);
        frm.openDialog;
    }
    scope.set_job_w_hold_code = function () {
        var frm = lv.FormSearch(scope, "$$$job_w_hold");
        frm.JobWorking(scope.entity, "job_w_hold_code", "${get_res('job_w_hold_code','Chức danh kiêm nhiệm')}", false);
        frm.openDialog;
    }

    function onSave() {
        if (scope.entity != null) {
            //if (scope.entity.active == null || scope.entity.active == undefined) {
            //    scope.entity.active = true;
            //}
            //scope.entity.active = (scope.entity.active) ? false : true;
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result) {
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);//Xuất thông báo thành cônng
                    if (scope.__mode == 1 || scope.__mode == 3) {
                        //Reload table data
                        reloadData();
                        //unlock menuItem
                        $('.zb-left-li').css("pointer-events", "all");
                    }

                    else if (scope.__mode == 2) {
                        scope.$parent.$parent.$parent.currentItem.full_name = res.entity.last_name + " " + res.entity.first_name;
                        scope.$parent.$parent.$parent.currentItem.gender = _.findWhere(scope.$parent.$parent.$parent.cbbGender, { "value": res.entity.gender })['caption'];
                        scope.$parent.$parent.$parent.currentItem.department_name = res.entity.department_name;
                        scope.$parent.$parent.$parent.currentItem.job_w_code = res.entity.job_w_code;
                        scope.$parent.$parent.$parent.currentItem.join_date = res.entity.join_date;
                        //Refesh datatable
                        scope.$parent.$parent.$parent.refreshDataRow();
                        scope.$parent.$parent.$parent.$apply();
                    }
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            });
        }
    }

    function onAttach() {
        alert('onAttach');
    }

    function onPrint() {
        alert('onAttach');
    }

    function onRefresh() {
        alert('onAttach');
    }

    function editData(callback) {
        var url = getUrl();
        var currentItem = JSON.parse(JSON.stringify(scope.entity));
        services.api(url)
            .data(currentItem)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function beforeCallToServer() {

    }

    function getUrl() {
        return scope.__mode == 1 || scope.__mode == 3 ? "${get_api_key('app_main.api.HCSEM_Employees/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.HCSEM_Employees/update')}" /*Mode 2: Cập nhật*/
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.employee_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('employee_code_is_not_null','Mã nhân viên không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.last_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('last_name_is_not_null','Họ không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.first_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('first_name_is_not_null','Tên không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.join_date);
        rs.result = valid.isDate();
        rs.errorMsg = rs.result === false ? "${get_res('join_date_is_not_null','Ngày vào làm không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            rs.result = true;
            return rs;
        } else {
            rs.result = false;
        }
        valid = lv.Validate(scope.entity.department_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('department_code_is_not_null','Bộ phận làm việc không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.job_w_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_code_is_not_null','Chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        return rs;
    }

    function reloadData() {
        scope.$parent.$parent.$parent.refresh();
    }

    function _getEmployee(empCode) {
        if (scope.__mode == 2) {
            services.api("${get_api_key('app_main.api.HCSEM_Employees/get_employee_by_emp_code')}")
                .data({
                    "employee_code": empCode
                })
                .done()
                .then(function (res) {
                    //res.active = (res.active) ? false : true;
                    scope.entity = res;
                    _getDataInitCombobox();
                    scope.$applyAsync();
                })
        }
    }

    $(document).ready(function () {
        $('#email').focusout(function (e) {
            if ($(this).val() != "") {
                var rs = true;
                var valid = lv.Validate(scope.entity.email);
                rs = valid.isEmail();
                if (rs !== true) {
                    $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", "${get_global_res('email_is_not_valid','Email không hợp lệ')}", function () { });
                    $(this).focus();
                }
            }
        })

        $('#personal_email').focusout(function (e) {
            if ($(this).val() != "") {
                var rs = true;
                var valid = lv.Validate(scope.entity.personal_email);
                rs = valid.isEmail();
                if (rs !== true) {
                    $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", "${get_global_res('personal_email_is_not_valid','Email cá nhân không hợp lệ')}", function () { });
                    $(this).focus();
                }
            }
        })
    })

    function _init_() {
        scope.__mode = scope.$parent.$parent.$parent.mode;
    }

    scope.$parent.$parent.$parent.$watch("mode", function (val) {
        if (val != 0)
            _init_();
    })

    scope.$parent.$parent.$parent.$watchGroup(['mode', 'currentItem'], function (val) {
        if (val[0] != 0) {
            //scope.$active = (val[1].active != undefined) ? val[1].active : true;
            //scope.$root.$commons.$active = scope.$active;
            scope.$parent.$parent.$parent.onSave = onSave;
            _init_();
            
            if (val[0] == 2) {
                _getEmployee(val[1].employee_code);
                $('.zb-left-li').css("pointer-events", "all");
                scope.$applyAsync();
            } else if (val[0] == 1) {
                scope.entity = {};
                _getDataInitCombobox();
                $('.zb-left-li').css("pointer-events", "none");
                scope.$applyAsync();
            }
        }
    })

    scope.$root.$watch('$commons.$current_employee_code', function(val){
        if(val){
            _getEmployee(val);
            $('.zb-left-li').css("pointer-events", "all");
            scope.$applyAsync();
        }
    });

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('cbb_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('b_province_code')
                    ? scope.entity.b_province_code
                    : null,
                "alias": "$$$b_cbb_province"
            },
            {
                "key": "${encryptor.get_key('cbb_nation')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('nation_code')
                    ? scope.entity.nation_code
                    : null,
                "alias": "$$$cbb_nation"
            },
            {
                "key": "${encryptor.get_key('cbb_ethnic')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('ethnic_code')
                    ? scope.entity.ethnic_code
                    : null,
                "alias": "$$$cbb_ethnic"
            },
            {
                "key": "${encryptor.get_key('cbb_religion')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('religion_code')
                    ? scope.entity.religion_code
                    : null,
                "alias": "$$$cbb_religion"
            },
            {
                "key": "${encryptor.get_key('cbb_acadame')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('train_level_code')
                    ? scope.entity.train_level_code
                    : null,
                "alias": "$$$cbb_acadame"
            },
            {
                "key": "${encryptor.get_key('cbb_marital')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('marital_code')
                    ? scope.entity.marital_code
                    : null,
                "alias": "$$$cbb_marital"
            },
            {
                "key": "${encryptor.get_key('cbb_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('p_province_code')
                    ? scope.entity.p_province_code
                    : null,
                "alias": "$$$p_cbb_province"
            },
            {
                "key": "${encryptor.get_key('cbb_district_of_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('p_district_code')
                    ? scope.entity.p_district_code
                    : null,
                "alias": "$$$p_cbb_district"
            },
            {
                "key": "${encryptor.get_key('cbb_ward_of_district')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('p_ward_code')
                    ? scope.entity.p_ward_code
                    : null,
                "alias": "$$$p_cbb_ward"
            },
            {
                "key": "${encryptor.get_key('cbb_hamlet_of_ward')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('p_hamlet_code')
                    ? scope.entity.p_hamlet_code
                    : null,
                "alias": "$$$p_cbb_hamlet"
            },
            {
                "key": "${encryptor.get_key('cbb_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('t_province_code')
                    ? scope.entity.t_province_code
                    : null,
                "alias": "$$$t_province_code"
            },
            {
                "key": "${encryptor.get_key('cbb_district_of_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('t_district_code')
                    ? scope.entity.t_district_code
                    : null,
                "alias": "$$$t_district_code"
            },
            {
                "key": "${encryptor.get_key('cbb_ward_of_district')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('t_ward_code')
                    ? scope.entity.t_ward_code
                    : null,
                "alias": "$$$t_ward_code"
            },
            {
                "key": "${encryptor.get_key('cbb_hamlet_of_ward')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('t_hamlet_code')
                    ? scope.entity.t_hamlet_code
                    : null,
                "alias": "$$$t_hamlet_code"
            },
            {
                "key": "${encryptor.get_key('cbb_province')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('issued_place_code')
                    ? scope.entity.issued_place_code
                    : null,
                "alias": "$$$issued_place_code"
            },
            {
                "key": "${encryptor.get_key('cbb_employee_type')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('emp_type_code')
                    ? scope.entity.emp_type_code
                    : null,
                "alias": "$$$emp_type_code"
            },
            {
                "key": "${encryptor.get_key('cbb_departments')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('department_code')
                    ? scope.entity.department_code
                    : null,
                "alias": "$$$department_code"
            },
            {
                "key": "${encryptor.get_key('cbb_position')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_pos_code')
                    ? scope.entity.job_pos_code
                    : null,
                "alias": "$$$job_pos_code"
            },
            {
                "key": "${encryptor.get_key('cbb_profession')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('profession_code')
                    ? scope.entity.profession_code
                    : null,
                "alias": "$$$profession_code"
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
                    && scope.entity.hasOwnProperty('manager_sub_code')
                    ? scope.entity.manager_sub_code
                    : null,
                "alias": "$$$manager_sub_code"
            },
            {
                "key": "${encryptor.get_key('cbb_auth_user_info_no_filter')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('user_id')
                    ? scope.entity.user_id
                    : null,
                "alias": "$$$user_id"
            },
            {
                "key": "${encryptor.get_key('cbb_position')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_pos_hold_code')
                    ? scope.entity.job_pos_hold_code
                    : null,
                "alias": "$$$job_pos_hold_code"
            },
            {
                "key": "${encryptor.get_key('cbb_departments')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('department_code_hold')
                    ? scope.entity.department_code_hold
                    : null,
                "alias": "$$$department_code_hold"
            },
            {
                "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('signed_person')
                    ? scope.entity.signed_person
                    : null,
                "alias": "$$$signed_person"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_single_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_w_code')
                    ? scope.entity.job_w_code
                    : null,
                "alias": "$$$job_working"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_single_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_w_hold_code')
                    ? scope.entity.job_w_hold_code
                    : null,
                "alias": "$$$job_w_hold"
            }
            ]

        );
    }
});