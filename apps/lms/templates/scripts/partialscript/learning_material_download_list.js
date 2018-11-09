﻿(function (scope) {

    scope.urls = scope.$root.url_static;
    scope.$root.extendToolbar = true;
    scope.$root.isDisplayManagermentButton = false;
    scope.$root.isDisplayBasicButton =false;
    scope.$root.isDisplay = false;
    scope.$root.isDisplayMoreButton = false;
    scope.__tableSource = [];
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.mapName = [];

    scope.$parent.$parent.$parent.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
            { "data": "material_id", "title": "${get_res('material_id_table_header','ID')}" },
            { "data": "material_name", "title": "${get_res('material_name_table_header','File Name')}"
                            , "format": "icon", "type": "link", "icon": "files", "position": "left" },
            { "data": "material_type", "title": "${get_res('material_type_table_header','File Type')}" },
            { "data": "size_files", "title": "${get_res('Size_table_header','Size')}" },
            { "data": "creator", "title": "${get_res('creator_table_header','Created by')}"
                            ,"expr":function(row, data, func){
                func(function(){
                    return "<img class='hcs-small-img' src='" + scope.urls + "css/icon/approver_tr.png" + "'/>"+ " " + row.creator ;

                });
                return true;
            } },
            { "data": "num_downloads", "title": "${get_res('Number_download_table_header','No. of Download')}", "className": "text-center" },
            { "data": "last_downloads", "title": "${get_res('latest_download_table_header','Latest Downloaded on')}","format": "date:" + scope.$root.systemConfig.date_format + ' hh:mm:ss a' },
        
    ];
    scope.$$tableConfig = {};
    scope.$root.$$tableConfig = {};
    scope.$root._tableData = _tableData;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        scope.$root.edit();
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    //scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = refresh;
    scope.$root.refresh = refresh;

    //function button
    scope.refresh = refresh;

    //Navigation: quay trở về UI list
    scope.backPage = backPage;

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 0;
            $(window).trigger('resize');
        }, 500);
    }

    function refresh() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function tableFields() {
        return [
            { "data": "material_id", "title": "${get_res('material_id_table_header','ID')}" },
            { "data": "material_name", "title": "${get_res('material_name_table_header','File Name')}" },
            { "data": "material_type", "title": "${get_res('material_type_table_header','File Type')}" },
            { "data": "size_files", "title": "${get_res('Size_table_header','Size')}" },
            { "data": "creator", "title": "${get_res('creator_table_header','Created by')}" },
            { "data": "num_downloads", "title": "${get_res('Number_download_table_header','No. of Download')}" },
            { "data": "last_downloads", "title": "${get_res('latest_download_table_header','Latest Downloaded on')}", "format": "date:" + 'dd/MM/yyyy h:mm:ss a' },
        ];
    }


    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
	};

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
			searchText: searchText

        };
        scope.$root.$$tableConfig = {
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

	scope._tableData = _tableData;
    function _tableData(iPage, iPageLength, orderBy, searchText, callback, objSearchAdvance) {
        
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_list_download_history')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
					"sort": sort,
                })
                .done()
            .then(function (res) {
                    
                    var resData = _.map(res.items, function (num) {
                        num.size_files = num.size_files + "KB";
                        return num;
                    });
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: resData
                    };
                    scope.__tableSource = JSON.parse(JSON.stringify(resData));
					scope.ItemTables = JSON.parse(JSON.stringify(resData));
					var total_rating = 0;
					for (var i = 0; i < scope.ItemTables.length; i++) {
						var Ratings = [];
						if (data.data[i].comments == null) {
							data.data[i]["total_rating"] = 0;
						}
						else if (data.data[i].comments && data.data[i].comments.length > 0) {
							for (var j = 0; j < data.data[i].comments.length; j++) {
								Ratings.push(data.data[i].comments[j].rating)
							}
							var sum = Ratings.reduce((previous, current) => current += previous);
							data.data[i]["total_rating"] = sum / Ratings.length;
						}
					}
					scope.ItemTables = JSON.parse(JSON.stringify(data.data));
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
        //}
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }

    scope.$watch("$parent.searchText", function (val) {
        
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, val)

        scope.$applyAsync();
    });
});
