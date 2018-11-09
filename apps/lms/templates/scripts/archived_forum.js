(function (scope){

    scope.selectedItems = [];

    scope.$parent.$parent.$parent.edit = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('edit_pl_forum','Edit Public Forum')}", 'form/addForumPublic', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.$parent.$parent.$parent.delete = function () {
        scope.mode = 3;
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Forum/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {

                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    };

    scope.$parent.$parent.$parent.update_status_open = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Update_Status','Bạn có muốn cập nhật lại trạng thái không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Forum/update_status_open')}")
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

    scope.$parent.$parent.$parent.update_status_suspend = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Update_Status','Bạn có muốn cập nhật lại trạng thái không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Forum/update_status_suspend')}")
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

    scope.$parent.$parent.$parent.update_status_write_protected = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Update_Status','Bạn có muốn cập nhật lại trạng thái không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_Forum/update_status_write_protected')}")
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



    scope.onSelectTableRow = function ($row) {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('edit_lms_forum','Edit Forum')}", 'form/addForumPublic', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }


      /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
            { "data": "forum_id", "title": "${get_res('forum_id','ID')}" },
            { "data": "forum_name", "title": "${get_res('forum_name','Forum Name')}" },
            { "data": "description", "title": "${get_res('forum_description','Description')}" },
            { "data": "forum_typeName", "title": "${get_res('forum_type','Forum Type')}","expr":function(row, data, func){
                func(function(){
                    return "<div style='color:#5B9BD5'>" + " " + row.forum_typeName + "</div>";
                });
                return true;
            }},
            { "data": "avail_start_date", "title": "${get_res('forum_start_date','Start Date')}", "className": "text-center" ,"expr":function(row, data, func){
                func(function(){
                    if(data != null)
                        return "<image style='width:16px;height:16px;margin-bottom:3px' src='" +  scope.$root.url_static + "css/icon/calendar.png'/>" +" " + window.DateFormat.format(data, scope.$root.systemConfig.date_format);
                    return " ";
                });
                return true;
            }},
            { "data": "avail_end_date", "title": "${get_res('forum_end_date','End Date')}", "className": "text-center" ,"expr":function(row, data, func){
                func(function(){
                    if(data != null)
                        return "<image style='width:16px;height:16px;margin-bottom:3px' src='" +  scope.$root.url_static + "css/icon/calendar.png'/>" +" " + window.DateFormat.format(data, scope.$root.systemConfig.date_format);
                    return " ";
                });
                return true;
            }},
            { "data": "forum_administrator_name", "title": "${get_res('forum_administrator','Forum Admin')}" ,"expr":function(row, data, func){
                func(function(){
                    if(data != null)
                        return "<img style='width:15px;height:17px' src='" + scope.$root.url_static + "css/icon/approver_tr.png" + "'/>" + " " + data;
                    return " ";
                });
                return true;
            }},
            { "data": "statusName", "title": "${get_res('forum_statusName','Status')}","expr":function(row, data, func){
                func(function(){
                    if(row.statusName != "")
                        return "<div class='" + row.styleRadio + "'></div>" + "<i class='" + row.styleText+ "'>" + row.statusName + "</i>";
                    return "<i style='width:15px;height:17px;font-weight:900'>" + " " + row.status + "</i>";
                });
                return true;
            }},
            { "data": "created_on", "title": "${get_res('forum_created_on','Create At')}","format": "date:" +  scope.$root.systemConfig.date_format + ' h:mm:ss a' },
    ];


    scope.tableSource = _loadDataServerSide;

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$root.$$tableConfig = scope.$$tableConfig = {
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

    scope.$root._tableData = scope._tableData = _tableData;
    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "desc") ? -1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_Forum/get_list_with_searchtext_archived')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    _.map(res.items, function(it) {
                        switch (it.forum_status) {
	                    case 1:
	                    	it.statusName = "${get_global_res('open','Open')}";
	                    	it.styleRadio = "status-radio-green";
	                    	it.styleText = "status-text-green";
	                    	break;
	                    case 2:
	                    	it.statusName = "${get_global_res('suspend','Suspend')}";
	                    	it.styleRadio = "status-radio-red";
	                    	it.styleText = "status-text-red";
	                    	break;
	                    case 3:
	                    	it.statusName = "${get_global_res('write_protected','Write Protected')}";
	                    	it.styleRadio = "status-radio-yellow";
	                    	it.styleText = "status-text-yellow";
	                    	break;
	                    default:
	                        it.statusName = "";
                        }

                        switch (it.forum_type) {
	                    case true:
	                    	it.forum_typeName = "${get_global_res('public','Public')}";
	                    	break;
	                    case false:
	                    	it.forum_typeName = "${get_global_res('private','Private')}";
	                    	break;
                         default:
	                        it.forum_typeName = "";
                        }

                        return it;
                    })

                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);

                    //

                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    scope.refreshDataRow = refresh;

    function refresh() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }



});
