(function(scope){
    scope.listViewAprPeriod = [{
        aprName: 'Tháng 1/2018',
        giveTargetDate:{
            from: new Date,
            to: new Date
        },
        delayGiveTargetDate:{
            from: new Date,
            to: new Date
        },
        assignDate: new Date,
        aprCode: "1-2018"
    },
    {
        aprName: "Tháng 2/2018",
        giveTargetDate:{
            from: new Date,
            to: new Date
        },
        delayGiveTargetDate:{
            from: new Date,
            to: new Date
        },
        assignDate: new Date,
        aprCode: "2-2018"
    },
    {
        aprName: "Tháng 3/2018",
        giveTargetDate:{
            from: new Date,
            to: new Date
        },
        delayGiveTargetDate:{
            from: new Date,
            to: new Date
        },
        assignDate: new Date,
        aprCode: "3-2018"
    }];

    scope.selectApr = function(apr){
        scope._currentApr = apr;
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
        if(scope._currentEmp){

        }else{
            callback({
                recordsTotal: 0,
                recordsFiltered: 0,
                data: []
            })
        }
    }

    function openGenData(){
        scope.$root.$extension.openDialog(scope, "${get_res('generate_data', 'Phát sinh dữ liệu')}", "giveTarget/form/portalGenData", function(){});
    }

    function openDetailData(){
        scope.$root.$extension.openDialog(scope, "${get_res('target_detail', 'Chi tiết mục tiêu')}", "giveTarget/form/portalDetail", function(){});
    }
});