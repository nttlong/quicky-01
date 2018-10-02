(function (scope) {
    var _default = {
        com_code: "",
        com_name: "",
        com_name2: "",
        com_group_code: scope.$parent.$parent.$$tree.treeCurrentNode.com_group_code,
        com_type: 3,
        apr_form_type: 1,
        point_scale_type: 1,
        score_from: "",
        score_to: "",
        bu_codes: "",
        com_desc: "",
        note: "",
        ordinal: "",
        lock: false
    };
    scope.__mode = scope.$parent.mode;
    scope.$parent.saveNNext = saveNNext;
    scope.set_job_working = set_job_working;

    function set_job_working() {
        var frm = lv.FormSearch(scope, "$$$job_working");
        frm.JobWorking(scope.entity, "job_working", "${get_res('job_w_next','CDCV thuyên chuyển')}", true);
        //frm.openDialog;
    }

    function saveNNext() {
        if (scope.entity != null) {
            var rsCheck = checkError();
            if (rsCheck.result) {
                $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                return;
            }
            beforeCallToServer();
            editData(function (res) {
                if (res.error == null) {
                    reloadData();
                    $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                    // scope.entity = null;
                    // scope.__mode = 1;
                    scope.$parent.mode = 2;
                    scope.$parent.$com_code = scope.entity.com_code;
                    scope.$parent.$apply();
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

    }

    function getUrl() {
        return scope.__mode == 1 || scope.__mode == 3 ? "${get_api_key('app_main.api.TMLS_Competency/insert')}"
            : "${get_api_key('app_main.api.TMLS_Competency/update')}"
    }

    function reloadData() {
        var tableConfig = scope.$parent.$parent.$$table.$$tableConfig;
        scope.$parent.$parent._tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.com_code);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('com_code_is_not_null','Mã không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.com_name);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('com_name_is_not_null','Tên năng lực không được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        valid = lv.Validate(scope.entity.com_type);
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('com_type_is_not_null')}" : "Phân loại không được để trống" ;
        if (rs.result === false) {
            rs.result = true;
            return rs;
        } else {
            rs.result = false;
        }
        valid = lv.Validate(scope.entity.apr_form_type);
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('apr_form_type_is_not_null')}" : "Hình thức đánh giá không được để trống";
        if (rs.result === false) {
            rs.result = true;
            return rs;
        } else {
            rs.result = false;
        }
        valid = lv.Validate(scope.entity.point_scale_type);
        rs.result = valid.isNumber();
        rs.errorMsg = rs.result === false ? "${get_res('point_scale_type_is_not_null')}" : "Áp dụng thang điểm không được để trống";
        if (rs.result === false) {
            rs.result = true;
            return rs;
        } else {
            rs.result = false;
        }
        return rs;
    }

    function _getCompetencyByComCode(code, callback) {
        services.api("${get_api_key('app_main.api.TMLS_Competency/get_by_com_code')}")
            .data({
                "competency": code
            })
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function _getValueList() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                    "PERF_Competency_Type",
                    "PERF_AproveFormType",
                    "PERF_PointScaleType"
                ]
            })
            .done()
            .then(function (res) {
                scope.cbbCompetencyType = getValue(res.values, "PERF_Competency_Type");
                scope.cbbCompetencyType.shift();
                scope.cbbAproveFormType = getValue(res.values, "PERF_AproveFormType");
                scope.cbbPointScaleType = getValue(res.values, "PERF_PointScaleType");
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
    };

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('cbb_tmls_competency_group')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('com_group_code')
                    ? scope.entity.com_group_code
                    : null,
                "alias": "$$$cbb_tmls_competency_group"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_multi_check')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('job_working')
                    ? scope.entity.job_working
                    : null,
                "alias": "$$$job_working"
            }]
        );
    };

    (function __initialize__() {
        if (scope.__mode == 1) {
            scope.entity = _default;
            _getDataInitCombobox();
            _getValueList();
        }
        else {
            _getCompetencyByComCode(scope.$parent.$com_code, function (val) {
                if (!val.hasOwnProperty('error')) {
                    scope.entity = val;
                    _getDataInitCombobox();
                    _getValueList();
                } else {
                    $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                }
            })
        }
    })();
});