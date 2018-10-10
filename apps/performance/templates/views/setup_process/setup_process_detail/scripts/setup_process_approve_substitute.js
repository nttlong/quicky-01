(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "process_code", "title": "${get_res('process_code','Mã người duyệt')}", "className": "text-left" },
            { "data": "process_name", "title": "${get_res('process_name','Tên người duyệt')}", "className": "text-left" },
            { "data": "substitute_code", "title": "${get_res('substitute_code','Mã người thay thế')}", "className": "text-left" },
            { "data": "substitute_name", "title": "${get_res('substitute_name','Tên người thay thế')}", "className": "text-left" },
            { "data": "from_date", "title": "${get_res('from_date','Hiệu lực từ ngày')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "to_date", "title": "${get_res('to_date','Đến ngày')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    scope.__mode = scope.$parent.$parent.$parent.$parent.mode;
    scope.$$process_id = scope.__mode == 2 ? scope.$parent.$parent.$parent.$parent.$$table.currentItem.process_id : null;

    scope._tableData = _tableData;
    scope.reloadData = reloadData;
    scope.mode = 0;
    scope.searchText = "";

    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onSave = null;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = reloadData;
    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.onRefresh = function(){
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
    };
    function onSearch(val) {
    debugger
        scope.$$table.tableSearchText = val;
        scope.$apply();
    }
//    function pressEnter($row) {
//        scope.onEdit();
//    }

    function onAdd() {
            scope.mode = 1;
            openDialog("${get_res('Factor_Appraisal','Chi tiết ủy quyền duyệt thay')}", 'setup_process/setup_process_detail/form/addSetupProcessApproverSubstitute', function () { });
    };

    function onEdit() {
        if (Object.keys(scope.$$table.currentItem).length > 0) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('detail_approver_1','Chi tiết ủy quyền duyệt thay')}" , 'setup_process/setup_process_detail/form/addSetupProcessApproverSubstitute', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onSave() {
    debugger
       if (scope.entity !== null) {
                services.api("${get_api_key('app_main.api.TM_SetupProcessApproverSubstitute/save')}")
                    .data(param)
                    .done()
                    .then(function (res) {
                        if (res.error === null) {
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                        } else {
                            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", function () { });
                        }
                        scope.$applyAsync();
                    });
        }
    }
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TM_SetupProcessApproverSubstitute/delete')}")
                    .data({
                        process_id : scope.$$process_id,
                        _id : _.pluck(scope.$$table.selectedItems, "_id")
                    })
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            reloadData();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }

    };
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });

    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TM_SetupProcessApproverEmp'
            }).done();

    };
    function onAttach() {

    };
    function reloadData(){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
    }

    (function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [
            {
                "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('approver_code')
                    ? scope.entity.approver_code
                    : null,
                "alias": "$$$approver_code"
            },

            {
                "key": "${encryptor.get_key('cbb_employees_cbcc')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('substitute_code')
                    ? scope.entity.substitute_code
                    : null,
                "alias": "$$$substitute_code"
            }
            ]

        );
    })();

     function openDialog(title, path, callback, id = 'myModal') {

        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }
    scope.$parent.$watch("advancedSearch.data_lock", function (val) {
        var config = scope.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    });

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$table.$$tableConfig = {
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

    //
    scope.tableSearchText = '';
    scope.SearchText = '';

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "desc") ? -1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.TM_SetupProcessApproverSubstitute/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "process_id": scope.$$process_id
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

});