﻿(function (scope) {
    var _default = {
        rec_id : null,
        email_template_code : null,
        email_template_name : null,
        description : null,
        subject : null,
        body : null,
        module_name : null
    }
    scope.mode = 0;
    scope.valueListModule = [];
    scope.dataSource = [];
    scope.searchText = "";
    scope.currentRow = {};

    scope.selectRow  = function(event, item){
        scope.mode = 2;
        scope.currentRow = JSON.parse(angular.toJson(item))
        scope.entity = JSON.parse(JSON.stringify(scope.currentRow));
    }

    scope._equal = function (TSource, Tdes) {
        return _.isEqual(JSON.parse(angular.toJson(TSource)), JSON.parse(angular.toJson(Tdes)))
    }

    scope.event = {
        add: function () {
            scope.mode = 1;
            scope.entity = null;
            scope.currentRow = null;
            scope.$apply();
        },
        save: function () {
            if (scope.entity != null) {
            var rsCheck = checkError();
            if (rsCheck.result) {
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            editData(function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    _getList();
                } else if(res.error.code == "missing"){
                    $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", "${get_res('action_is_not_null','Hành vi chuẩn không được để trống')}", function () { });
                }else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            });
        }
        },
        delete: function () {
            if (!scope.currentRow || Object.keys(scope.currentRow).length === 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            } else {
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                    services.api("${get_api_key('app_main.api.HCSSYS_EmailTemplate/delete')}")
                        .data(scope.currentRow)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                _getList();
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            } else if (res.error !== null || res.error !== "") {
                                $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_is_using','CDCV đang được sử dụng')}", function () { });
                            }
                        })
                });
            }
        },
        attach: function () {
            
        }
    }

    function editData(callback) {
        debugger
        var url = getUrl();
        var param = _.mapObject(_default, function(val, key) { return val = scope.entity[key] ? scope.entity[key] : null });
        param.body = param.body && param.body.hasOwnProperty('en') ? param.body.en : param.body;
        services.api(url)
            .data(param)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.email_template_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('email_template_code_is_not_null','Mã mẫu email không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.email_template_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('email_template_name_is_not_null','Tên mẫu email không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.module_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('module_name_is_not_null','Phân hệ không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.subject);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('subject_is_not_null','Tiêu đề không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        return rs;
    }

    function getUrl(){
        return scope.mode == 2 ? "${get_api_key('app_main.api.HCSSYS_EmailTemplate/update')}"
        : "${get_api_key('app_main.api.HCSSYS_EmailTemplate/insert')}";
    }

    function _getValueList(callback) {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name":"PERF_Module"
            })
            .done()
            .then(function (res) {
                callback(res)
            })
    }

    function _getList(){
        services.api("${get_api_key('app_main.api.HCSSYS_EmailTemplate/get_list')}")
            .data()
            .done()
            .then(function (res) {
                scope.dataSource = res;
                scope.$applyAsync();
            })
    }

    (function _init_() {
        _getList();
        _getValueList(function(res){
            scope.valueListModule = res.values;
            scope.$applyAsync();
        });
    })();
});