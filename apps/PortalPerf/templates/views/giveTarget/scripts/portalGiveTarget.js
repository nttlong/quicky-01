(function(scope){
    scope.$employee = [{employee_code:"NV001"}, {employee_code:"NV002"}, {employee_code:"NV003"}]
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
        //loadDataFilterEmployee();
    }

    scope.selectEmployee = function(emp){
        scope._currentEmp = emp;
        scope._currentEmpCode = emp.employee_code;
        //reloadData();
    }

    scope.openGenData = openGenData;
    scope.openDetailData = openDetailData;

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
        callback({
                recordsTotal: 0,
                recordsFiltered: 0,
                data: []
            });
    }

    function openGenData(){
        scope.$root.$extension.openDialog(scope, "${get_res('generate_data', 'Phát sinh dữ liệu')}", "giveTarget/form/portalGenData", function(){});
    }

    function openDetailData(){
        scope.$root.$extension.openDialog(scope, "${get_res('target_detail', 'Chi tiết mục tiêu')}", "giveTarget/form/portalDetail", function(){});
    }
});