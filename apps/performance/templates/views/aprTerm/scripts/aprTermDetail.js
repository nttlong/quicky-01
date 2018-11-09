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
            { "data": "perform", "title": "${get_res('perform','Thực hiện')}", "className": "text-center" },
            { "data": "complete_pct", "title": "${get_res('complete_pct','% Hoàn thành')}", "className": "text-center"},
            { "data": "person_1", "title": "${get_res('person_1','Nguyễn Văn A')}", "className": "text-center"},
            { "data": "person_2", "title": "${get_res('person_2','Lê Minh')}", "className": "text-center"},
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

    scope.changeTab = function(event){
        $('#tab_right').find('.active').removeClass('active');
        $(event.target).closest('div').addClass('active');
    }

    scope.changeActive = function(event, key){
        $('#tab_left').find('.active').removeClass('active');
        $('#tab_left').find('.approver').removeClass('approver');
        $('#tab_left').find('.waiting_approver').removeClass('waiting_approver');
        $('#tab_left').find('.deny').removeClass('deny');
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

    scope.onAdd = function(){
        scope.mode = 1;
        scope.$root.$extension.openDialog(scope, "${get_res('editTrainDetail','Chi tiết đề xuất đào tạo')}", "aprTerm/form/editTrainDetail", function(){});
    }

    scope.onEdit = function(){
        scope.mode = 2;
        scope.$root.$extension.openDialog(scope, "${get_res('editSurveyDetails','Chi tiết khảo sát')}", "aprTerm/form/editSurveyDetails", function(){});
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
                            val.person_1 = " ";
                            val.person_2 = " ";

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