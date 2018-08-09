(function (scope) {
    scope.$parent.$parent.$parent.$parent.detail.onSave = onSave;
    scope.__mode = scope.$parent.$parent.$parent.$parent.detail.$mode;
    scope.gjw_code = scope.$parent.$parent.$parent.$parent.detail.$gjw_code;
    //scope.gjw_name = scope.$parent.$parent.$parent.$parent.$$currentJobWorkingGroupName;

    scope.set_job_w_code = function () {
        var frm = lv.FormSearch(scope, "$$$job_working");
        frm.JobWorking(scope.entity, "job_w_change", "${get_res('job_w_change','CDCV có thể thuyên chuyển')}", true);
        frm.openDialog;
    }

    function onSave() {
        save();
    };

    function save() {
        if (scope.entity != null) {
            var rsCheck = checkError();//Kết quả check input
            if (rsCheck.result) {
                //Nhập sai: break khỏi hàm
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                if (res.error == null) {
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    scope.entity = res.data;
                    if (scope.__mode == 1)
                        scope.__mode = 2;
                    scope.$parent.$parent.$parent.currentJobWorkingName = res.data.job_w_name;
                    scope.$apply();
                } else {
                    $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                }
            })
        }
    }

    function editData(callback) {
        var url = getUrl();
        services.api(url)
            .data(scope.entity)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function beforeCallToServer() {
        scope.entity.gjw_code = scope.gjw_code;
    }

    function getUrl() {
        return scope.__mode == 1 ? "${get_api_key('app_main.api.HCSLS_JobWorking/insert')}" /*Mode 1: Tạo mới*/
            : "${get_api_key('app_main.api.HCSLS_JobWorking/update')}" /*Mode 2: Cập nhật*/
    }

    /**
     * Function check input
     */
    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.job_w_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_code_is_not_null','Mã chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.job_w_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_name_is_not_null','Tên chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.job_w_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('job_w_name_is_not_null','Tên chức danh không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        return rs;
    }

    function _getJobDescription(callback) {
        services.api("${get_api_key('app_main.api.HCSLS_JobWorking/get_job_description')}")
            .data({
                "job_w_code": scope.$parent.$parent.$parent.$parent.detail.$job_w_code
            })
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('cbb_position')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('province_code')
                    ? scope.entity.province_code
                    : null,
                "alias": "$$$cbb_position"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_multi_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_w_change')
                    ? scope.entity.job_w_change
                    : null,
                "alias": "$$$job_working"
            }]
        );
    }

    (function __init__() {
        if (scope.__mode == 2) {
            _getJobDescription(function (res) {
                scope.entity = res;
                _getDataInitCombobox();
                scope.$applyAsync();
            })
        }
    })();
});