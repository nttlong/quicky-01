(function(scope){
    scope.$filterEmployee = {status:1};
    var _currentEmpCode = null;
    var _currentAprPeriod = JSON.parse(JSON.stringify(scope.$parent.currentItem.apr_period.value));
    var _currentAprYear = JSON.parse(JSON.stringify(scope.$parent.currentItem.apr_year));
    scope._currentAprPeriod = _currentAprPeriod;
    scope._currentAprYear = _currentAprYear;
    scope._currentEmpCode = _currentEmpCode;
    scope.reloadData = reloadData;
    scope.loadDataFilterEmployee = loadDataFilterEmployee;
    scope.$$table = {
        tableFields: [
            { "data": "target_name", "title": "${get_res('target_name','Mục tiêu')}", "className": "text-left" },
            { "data": "unit_name", "title": "${get_res('DVT','Đơn vị tính')}", "className": "text-left" },
            { "data": "weight", "title": "${get_res('weight','Trọng số')}", "className": "text-left" },
            { "data": "target", "title": "${get_res('target','Chỉ tiêu')}", "className": "text-left" },
            { "data": "min_value", "title": "${get_res('min_value','Tối thiểu')}", "className": "text-center" },
            { "data": "max_value", "title": "${get_res('max_value','Tối đa')}", "className": "text-center"},
            { "data": "origin_target", "title": "${get_res('first_target','Chỉ tiêu ban đầu')}", "className": "text-center"}
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { scope.onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: '',
        refreshDataRow: function () { /*Do nothing*/ }
    }
    scope.backToMain = function(){
        scope.$parent.$display.showDetail = false;
        setTimeout(function(){
            $(window).trigger('resize');
        }, 100)
    }
    scope.changeActive = function(event, key){
        $('.hcs-tab-info').find('.active').removeClass('active');
        $('.hcs-tab-info').find('.approver').removeClass('approver');
        $('.hcs-tab-info').find('.waiting_approver').removeClass('waiting_approver');
        $('.hcs-tab-info').find('.deny').removeClass('deny');
        if(key == 1){
            $(event.target).closest('div').addClass('active');
        }
        else if (key==2){
            $(event.target).closest('div').addClass('approver');
            scope.$filterEmployee.status = 1;
        }
        else if (key==3){
            $(event.target).closest('div').addClass('waiting_approver');
            scope.$filterEmployee.status = 2;
        }
        else if (key==4){
            $(event.target).closest('div').addClass('deny');
            scope.$filterEmployee.status = 3;
        }
        loadDataFilterEmployee();
    }

    function loadDataFilterEmployee(){
        services.api("${get_api_key('app_main.api.TMPER_TargetKPI_EmpController/get_list')}")
                .data({
                    "apr_period": _currentAprPeriod,
                    "apr_year": _currentAprYear,
                    "status": scope.$filterEmployee.status,
                    "department_code": scope.$filterEmployee.department_code,
                    "job_w_code": scope.$filterEmployee.job_w_code
                })
                .done()
                .then(function (res) {
                    scope.listFilterEmployee = res;
                    scope._currentEmp = res.length > 0 ? res[0] : null;
                    $('#groupKPI span.zb-header-title.hcs-zb-header-title-custom').text(scope._currentEmp.employee_name);
                    scope.$applyAsync();
                })
    }

    function countEmployeeWithStatus(){
        services.api("${get_api_key('app_main.api.TMPER_TargetKPI_EmpController/count_employee')}")
                .data({
                    "apr_period": _currentAprPeriod,
                    "apr_year": _currentAprYear
                })
                .done()
                .then(function (res) {
                    scope.countEmployeeWithStatus = res;
                })
    }

    function reloadData(){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    }

    scope.filterEmployee = function(){
        loadDataFilterEmployee();
    }

    scope.selectEmployee = function(emp){
        scope._currentEmp = emp;
        scope._currentEmpCode = emp.employee_code;
        //reloadData();
    }

    scope.set_job_w_code = function () {
        var frm = lv.FormSearch(scope, "$$$job_working");
        frm.JobWorking(scope.$filterEmployee, "job_w_code", "${get_res('job_w_code','Chức danh')}", true);
        frm.openDialog;
    }

    scope.onGen = function(){
        scope.$root.$extension.openDialog(scope, "${get_res('generate_target_employee','Phát sinh mục tiêu nhân viên')}", "giveTarget/form/genGiveTarget", function(){});
    };

    scope.onAdd = function(){
        scope.mode = 1;
        if(scope._currentEmp)
            scope.$root.$extension.openDialog(scope, "${get_res('target_detail','Chi tiết mục tiêu')}" + " - " + scope._currentEmp.employee_name + " - " + scope.apr_name + "/" + _currentAprYear, "giveTarget/form/editGiveTarget", function(){});
        else
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_employee_selected','Chưa có nhân viên nào được chọn')}", function () { });
    }

    scope.onEdit = function(){
        scope.mode = 2;
        if(!scope.$$table.currentItem || Object.keys(scope.$$table.currentItem).length <= 0)
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_target_selected','Chưa có mục tiêu nào được chọn')}", function () { });
        else if(scope._currentEmp && (scope.$$table.currentItem && Object.keys(scope.$$table.currentItem).length > 0))
            scope.$root.$extension.openDialog(scope, "${get_res('target_detail','Chi tiết mục tiêu')}" + " - " + scope._currentEmp.employee_name + " - " + scope.apr_name + "/" + _currentAprYear, "giveTarget/form/editGiveTarget", function(){});
        else
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_employee_selected','Chưa có nhân viên nào được chọn')}", function () { });
    }

    scope.onDelete = function(){
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMPER_TargetKPIController/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            reloadData();
                        }
                    })
            });
        }
    }

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$table.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        if (fnReloadData) {
            if (searchText) {
                _tableData(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableData(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
    };

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        if(scope._currentEmp){
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.TMPER_TargetKPIController/get_list')}")
                    .data({
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "apr_period": _currentAprPeriod,
                        "apr_year": _currentAprYear,
                        "employee_code": scope._currentEmp.employee_code
                    })
                    .done()
                    .then(function (res) {
                        if (res.items) {
                            var data = {
                                recordsTotal: res.total_items,
                                recordsFiltered: res.total_items,
                                data: res.items
                            };
                            callback(data);
                            scope.$apply();
                        }
                    })
        }else{
            callback({
                recordsTotal: 0,
                recordsFiltered: 0,
                data: []
            })
        }
    }

    (function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('cbb_departments_multi_select')}",
                "code": null,
                "alias": "$$$department"
            },
            {
                "key": "${encryptor.get_key('cbb_job_working_multi_check')}",
                "code": null,
                "alias": "$$$job_working"
            }]
        );
    })();

    (function __init__(){
        loadDataFilterEmployee();
        countEmployeeWithStatus();
        scope.$root.$extension.getValueList("LApprovalPeriod", function(res){
            scope.LApprovalPeriod = res.values;
            scope.apr_name = _.findWhere(scope.LApprovalPeriod, {value: _currentAprPeriod}).caption;
        });
    })();

    scope.$watch('_currentEmp', function(val){
        reloadData();
    })
});