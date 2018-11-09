(function(scope){
    scope.$filterEmployee = {status:1};
    var _currentEmpCode = null;
    var _currentAprPeriod = JSON.parse(JSON.stringify(scope.$parent.currentItem.apr_period));
    var _currentAprYear = JSON.parse(JSON.stringify(scope.$parent.currentItem.apr_year));
    scope._currentAprPeriod = _currentAprPeriod;
    scope._currentAprYear = _currentAprYear;
    scope._currentEmpCode = _currentEmpCode;
    scope.reloadData = reloadData;
    scope.loadDataFilterEmployee = loadDataFilterEmployee;
    scope.$$table = {
        tableFields: [
            { "data": "target_name", "title": "${get_res('target_name','Mục tiêu')}", "className": "text-left" },
            { "data": "target", "title": "${get_res('target','Chỉ tiêu')}", "className": "text-left" },
            { "data": "min_value", "title": "${get_res('min_value','Tối thiểu')}", "className": "text-center" },
            { "data": "max_value", "title": "${get_res('max_value','Tối đa')}", "className": "text-center"},
            { "data": "perform", "title": "${get_res('perform','Thực hiện')}", "className": "text-center" },
            { "data": "complete_pct", "title": "${get_res('complete_pct','% Hoàn thành')}", "className": "text-center"},
            { "data": "update_status", "title": "${get_res('update_status','Tình trạng cập nhật')}", "className": "text-center"},
            { "data": "count_delay", "title": "${get_res('count_delay','Số lần trễ')}", "className": "text-center"},
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

    scope.onEdit = function(){
        scope.mode = 2;
        if(!scope.$$table.currentItem || Object.keys(scope.$$table.currentItem).length <= 0)
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_target_selected','Chưa có mục tiêu nào được chọn')}", function () { });
        else if(scope._currentEmp && (scope.$$table.currentItem && Object.keys(scope.$$table.currentItem).length > 0))
            scope.$root.$extension.openDialog(scope, "${get_res('target_detail','Chi tiết mục tiêu')}" + " - " + scope._currentEmp.employee_name + " - " + scope.apr_name + "/" + _currentAprYear, "updateTarget/form/editUpdateTarget", function(){});
        else
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_employee_selected','Chưa có nhân viên nào được chọn')}", function () { });
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
                services.api("${get_api_key('app_main.api.TMPER_TargetKPIController/get_list_update_target')}")
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
                        _.map(res.items, function(val) {
                            val.update_status = " ";
                            val.count_delay = " ";

                            return val;
                        })

                        if (res.items) {
                            var data = {
                                recordsTotal: res.total_items,
                                recordsFiltered: res.total_items,
                                data: res.items
                            };
                            scope.__tableSource = JSON.parse(JSON.stringify(res.items));
                            callback(data);
                            scope.currentItem = null;
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

    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableDetailFields = [
        { "data": "perform_date", "title": "${get_res('perform_date_table_header','Ngày tạo')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format },
        { "data": "perform", "title": "${get_res('perform','Thực hiện')}", "className": "text-center" },
        { "data": "note", "title": "${get_res('note_table_header','Kế hoạch hành động')}"},
    ];
    //
    scope.$$tableDetailConfig = {};


    //Dữ liệu cho table
    scope.tableDetailSource = _loadDetailDataServerSide;
    function _loadDetailDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableDetailConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableDetailData(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableDetailData(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };

     function _tableDetailData(iPage, iPageLength, orderBy, searchText, callback) {
        if(Object.keys(scope.$$table.currentItem).length > 0)
        {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.TMPER_TargetKPIDetailController/get_list')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "rec_id" : scope.$$table.currentItem.rec_id,
                    })
                    .done()
                    .then(function (res) {
                        var data = {
                            recordsTotal: res.total_items,
                            recordsFiltered: res.total_items,
                            data: res.items
                        };
                        callback(data);
                        scope.currentItem = null;
                        scope.$apply();
                    })

        }
    }

    scope.$watch("$$table.currentItem", function (val, old) {
        if (val != old && Object.keys(val).length > 0) {
            reloadDetailData();
            $('#groupKPIDetail span.zb-header-title.hcs-zb-header-title-custom').text("Chi tiết thực hiện: " + scope.$$table.currentItem.target_name);
        }
        else if(Object.keys(val).length == 0)
             {
                $('#groupKPIDetail span.zb-header-title.hcs-zb-header-title-custom').text("Chi tiết thực hiện:");
             }
    });

    function reloadDetailData() {
            var tableConfig = scope.$$tableDetailConfig;
            _tableDetailData(tableConfig.iPage,
                tableConfig.iPageLength, tableConfig.orderBy,
                tableConfig.searchText, tableConfig.fnReloadData);
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
        scope.$root.$extension.getValueList("LApprovalPeriod", function(res){
            scope.LApprovalPeriod = res.values;
            scope.apr_name = _.findWhere(scope.LApprovalPeriod, {value: _currentAprPeriod}).caption;
        });
    })();

    scope.$watch('_currentEmp', function(val){
        reloadData();
    })
});