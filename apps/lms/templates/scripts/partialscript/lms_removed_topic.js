﻿(function (scope) {
    scope.$root.extendToolbar = true;
    scope.$root.isDisplayBasicButton =true;

	scope.urls = scope.$root.url_static;
    scope.$root.isDisplay = false;
    scope.$root.isApprove = false;
    scope.__tableSource = [];
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.$parent.isDisplayGird = true;
    scope.$root.onDisplayListData = function () {
        scope.selectedItems = []
    }
    scope.$root.onDisplayGridData = function () {
        scope.selectedItems = []
    }
    scope.$root.add = function () {
        scope.mode = 1; // set mode chỉnh sửa
        openDialog("${get_res('Create_Topic','Create Topic')}", 'form/addTopic', function () {
            setTimeout(function () {
                $(window).trigger('resize');
            }, 200);
        });
    }
    
    scope.$root.edit = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Edit_Topic','Edit Topic')}", 'form/addTopic', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
            
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    scope.$root.delete = function () {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el && el._id
        })
        //
        if (scope.selectedItems.length > 0) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Topic/delete')}")
                    .data(arrayId)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.currentItem = [];
                            scope.$root.refresh();
                        }
                    })
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
	}

    scope.$root.pinTopic = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Pin_Topic','Bạn có muốn ghim topic không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Topic/update_topic_pin')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        scope.$applyAsync();
                        scope.currentItem = null;
                        scope.selectedItems = [];
                    })
            });
        }
    };

	scope.$root.blockTopic = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Block_Topic','Bạn có muốn khóa topic không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Topic/update_topic_block')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        scope.$applyAsync();
                        scope.currentItem = null;
                        scope.selectedItems = [];
                    })
            });
        }
    };

    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "topic_id", "title": "${get_res('topic_id','Topic ID')}" },
        { "data": "topic_name", "title": "${get_res('topic_name','Topic Name')}" },
        { "data": "topic_description", "title": "${get_res('topic_description','Topic Content')}" },
        { "data": "created_by", "title": "${get_res('created_by','Created by')}","expr":function(row, data, func){
            func(function(){
                return "<span><img class='hcs-small-img' style='width:15px;height:17px' src='" + scope.urls + "css/icon/approver_tr.png" + "'/>"
                + ' ' + row.created_by + ' ' +  window.DateFormat.format(row.created_on, 'dd.MM.yyyy hh:mm a')
                + '</span>';
            });
            return true;
        }},
        { "data": "topic_replies", "title": "${get_res('topic_replies','Replies')}" },
        { "data": "topic_views", "title": "${get_res('topic_views','Views')}" },
        { "data": "modified_by", "title": "${get_res('modified_by','Last Updated by')}","expr":function(row, data, func){
            func(function(){
                return "<span><img class='hcs-small-img' style='width:15px;height:17px' src='" + scope.urls + "css/icon/approver_tr.png" + "'/>"
                + ' ' + row.modified_by + ' ' +  window.DateFormat.format(row.modified_on, 'dd.MM.yyyy hh:mm a')
                + '</span>';
            });
            return true;
        }},
    ];
    scope.$$tableConfig = {};
    //scope.$root.$$tableConfig = {};
    //scope.$root._tableData = _tableData;
    //scope.$root._departments = _departments;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        scope.$root.edit();
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = refresh;
    scope.$root.refresh = refresh;

    /* Tree */
    scope.treeCurrentNode = {};
    scope.treeSelectedNodes = [];
    scope.treeSelectedRootNodes = [];
    scope.treeCheckAll = false;
    scope.treeSearchText = '';
    scope.treeDisable = false;
    scope.treeMultiSelect = false;
    scope.treeMode = 3; // Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
    var _treeDepartmentsDataSource = null;
    scope.treeDepartmentsDataSource = null;

    //navigation button
    scope.firstRow = firstRow;
    scope.previousRow = previousRow;
    scope.nextRow = nextRow;
    scope.lastRow = lastRow;

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
        _departments();
    }

    function firstRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[0];
        }
    }

    function previousRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === 0 ? scope.__tableSource.length - 1 : idx_item - 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function nextRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === (scope.__tableSource.length - 1) ? 0 : idx_item + 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function lastRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[scope.__tableSource.length - 1];
        }
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
        //setTimeout(function () {
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
        //}, 1000);
    };

	scope._tableData = _tableData;

    function _tableData(iPage, iPageLength, orderBy, searchText, callback, objSearchAdvance) {

        debugger

        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_Topic/get_list_with_searchtext_removed')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "where": {
						'forum_id': scope.treeCurrentNode.forum_id ? scope.treeCurrentNode.forum_id : null,
						'parent_code': scope.treeCurrentNode.parent_code ? scope.treeCurrentNode.parent_code : null
                    },
                    "sort": sort
                })
                .done()
            .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };

					scope.ItemTables = JSON.parse(JSON.stringify(data.data));
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        //if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        //}
    }

    ////////////////////////////////////////////////////////////////////////

    function _departments() {
        services.api("${get_api_key('app_main.api.LMSLS_Forum/get_list_tree_data')}")
            .data({})
            .done()
            .then(function (res) {
                _treeDepartmentsDataSource = [
                    {forum_id: "0", forum_name: "All forums", parent_code: null},
                    {forum_id: "1", forum_name: "Public Forums", parent_code: "0"},
                    {forum_id: "2", forum_name: "Private Forums", parent_code: "0"},
                    {forum_id: "3", forum_name: "Others", parent_code: null},
                ];
                _treeDepartmentsDataSource.push(...res.data);
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                scope.treeCurrentNode = _treeDepartmentsDataSource[0];
                scope.$applyAsync();

            })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }

    (function _init_() {
        _departments();
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
        scope.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("selectedFunction", function (function_id) {
        var $his = scope.$root.$history.data();
        if (scope.currentItem)
            window.location.href = "#page=" + $his.page + "&f=" + function_id;
    });

    scope.$watch("$parent.searchText", function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, val)  
        scope.$applyAsync();
    });


    scope.fnSelectDataGrid = fnSelectDataGrid;

    function fnSelectDataGrid(item) {
        scope.currentItem = item ? item : scope.currentItem;
        scope.$applyAsync();
    }

    scope.onCheckItemGird = function (item) {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el._id == item._id
        })
        if (arrayId.length > 0) {
            var arrayItem = scope.selectedItems.filter(function (el) {
                return el._id != item._id
            })
            scope.selectedItems = arrayItem;
        } else {
            scope.selectedItems.push(item);
        }

	}

    scope.$watch("treeCurrentNode", function(v, ov){
         if (v && ov != v)
         _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText, scope.$$tableConfig.fnReloadData);
    })


});