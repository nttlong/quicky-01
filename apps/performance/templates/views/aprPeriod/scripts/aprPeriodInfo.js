﻿(function (scope) {
    scope.__mode = scope.$parent.mode;


    scope.cbbApprovalPeriod = [];
    scope.$parent.$parent.$parent.onSave = onSave;

    scope.$parent.$parent.$parent.onAdd = "";
    scope.$parent.$parent.$parent.onEdit = "";
    scope.$parent.$parent.$parent.onDelete = "";
    scope.$parent.$parent.$parent.onImport = "";
    scope.$parent.$parent.$parent.onExport ="";
    scope.$parent.$parent.$parent.onAttach ="";
    scope.$parent.$parent.$parent.onRefresh ="";

    scope.$$tableConfig = {};
    scope.entity = {
        "_id": scope.$parent.entity._id,
        apr_year : scope.$parent.entity.apr_year,
    };
    function _comboboxData(callback) {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "LApprovalPeriod"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                 scope.cbbApprovalPeriod = res.values;
                if (callback ) callback(res);
                scope.$applyAsync();
            });
    }

    function onSave() {
    debugger
       if (scope.entity !== null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result === false) {
                //Nhập sai: break khỏi hàm
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
                var url = getUrl();
                services.api(url)
                    .data(scope.entity)
                    .done()
                    .then(function (res) {
                        if (res.error === null) {
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                            $('.zb-left-li').css("pointer-events", "all");
                            reloadData();
                            scope.$parent.apr_period_now = scope.entity.apr_period;
                            scope.$parent.apr_year_now = scope.entity.apr_year;
                            scope.$parent.mode = 2;
                        } else {
                            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                        }
                        scope.$applyAsync();
                    });
        }
    }

    function editData(callback) {
    services.api("${get_api_key('app_main.api.TMPER_AprPeriod/get_item_by_period_year')}")
        .data({
            apr_period: scope.entity.apr_period,
            apr_year: scope.entity.apr_year
        })
        .done()
        .then(function (res) {
            scope.$applyAsync();
            callback(res);
        });
    }

    function beforeCallToServer() {

    }

    function reloadData() {
        refresh();
        scope.$parent.entity.apr_period = scope.$parent.Map_Period(scope.entity.apr_period);
        scope.$parent.entity.apr_year = scope.entity.apr_year;
    }

    function getUrl() {
        return "${get_api_key('app_main.api.TMPER_AprPeriod/save')}";

    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.apr_period);
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('apr_period_is_not_null','Kỳ đánh giá không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('apr_year_is_not_null','Năm không được để trống')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        rs.result = check_year(scope.entity.apr_year);
        rs.errorMsg = rs.result === false ? "${get_res('apr_year_is_four_character','Năm phải bao gồm 4 ký tự số')}" + '\n' : "";
        if (rs.result === false) {
            return rs;
        }
        else if (new Date(scope.entity.give_target_from) > new Date(scope.entity.give_target_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('give_target_from_is_larger_give_target_to','Giao chỉ tiêu đến phải >= ngày giao chỉ tiêu từ')}";
        }
        else if (new Date(scope.entity.review_mid_from) < new Date(scope.entity.give_target_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('review_mid_from_is_larger_date_review_mid_to','Xem xét giữa kỳ từ phải >= ngày giao chỉ tiêu đến')}";
        }
        else if (new Date(scope.entity.approval_mid_from) > new Date(scope.entity.approval_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('approval_mid_to_is_larger_approval_mid_from','Xét duyệt giữa kỳ đến phải >= ngày xét duyệt giữa kỳ từ')}";
        }
        else if (new Date(scope.entity.approval_final_from) > new Date(scope.entity.approval_final_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('approval_final_to_is_larger_approval_final_from','Xét duyệt cuối kỳ đến phải >= ngày xét duyệt cuối kỳ từ')}";
        }
        else if (new Date(scope.entity.emp_final_from) > new Date(scope.entity.emp_final_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('emp_final_to_is_larger_emp_final_from','NV xét duyệt cuối kỳ đến phải >= ngày NV xét duyệt cuối kỳ từ')}";
        }
        else if (new Date(scope.entity.approval_mid_from) < new Date(scope.entity.review_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('approval_mid_from_larger_date_review_mid_to','Xét duyệt giữa kỳ từ phải >= Xem xét giữa kỳ đến')}";
        }
        else if (new Date(scope.entity.emp_final_from) < new Date(scope.entity.approval_mid_to)) {
            rs.result = false;
            rs.errorMsg = "${get_res('emp_final_from_is_not_null','NV đánh giá cuối kỳ từ phải >= ngày xét duyệt giữa kỳ đến')}";
        }
        else if (new Date(scope.entity.approval_final_from) < new Date(scope.entity.emp_final_to)){
            rs.result = false;
            rs.errorMsg = "${get_res('approval_final_from_is_not_null','Xét duyệt cuối kỳ từ phải >= ngày NV xét duyệt cuối kỳ đến')}";
        }

        return rs;
    }

    function check_year(numValid) {
        var a = numValid;
        if (a.toString().length == 4)
            return true;
        return false;
    }

    (function __init__() {
    debugger
        if (scope.__mode === 2) {
            scope.$root.$commons.$active = true;
            _comboboxData();

            services.api("${get_api_key('app_main.api.TMPER_AprPeriod/get_item_by_period_year')}")
            .data({
                apr_period: scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period),
                apr_year: scope.$parent.entity.apr_year
            })
            .done()
            .then(function (res) {
            scope.entity = res;
            scope.entity.apr_period = scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period);
                scope.$applyAsync();
            });


            }
       else if (scope.__mode === 1 || scope.__mode === 3) {
       $('.zb-left-li').css("pointer-events", "none");
        scope.$root.$commons.$active = true;
            _comboboxData(function(data){
                 scope.entity.apr_period = data.values[0].value;

                 scope.$applyAsync();
            });
            scope.entity.apr_year = (new Date()).getFullYear();
            scope.$applyAsync();
        }
    })();

    function refresh() {
        var tableConfig = scope.$parent.$$tableConfig;
        scope.$parent.tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData)
    }
});
