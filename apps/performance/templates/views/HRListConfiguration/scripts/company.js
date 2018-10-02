(function (scope) {
    var msgConfirm1 = "${get_res('msg_confirm_add_email1', 'Một số nhân viên đã được chọn thiết lập theo phòng ban')}" + ".";
    var msgConfirm2 = "${get_res('msg_confirm_add_email2', 'Bạn có muốn thay đổi luôn cho những nhân viên này theo toàn Cty?')}";

    scope.$$table = {
        tableFields: [
            { "data": "employee_code", "title": "${get_res('employee_code','Mã NV')}", "className": "text-left" },
            { "data": "full_name", "title": "${get_res('full_name','Họ tên')}", "className": "text-left" },
            { "data": "email_address", "title": "${get_global_res('email_address','Địa chỉ Email')}", "className": "text-left" },
            { "data": "note", "title": "${get_global_res('note','Ghi chú')}", "className": "text-left" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope._tableData = _tableData;
    scope.mode = 0;
    scope.searchText = "";
    scope.list_emp = [];

    scope.$parent.onSearch = onSearch;
    scope.$parent.onAdd = onAdd;
    scope.$parent.onEdit = onEdit;
    scope.$parent.onDelete = onDelete;
    scope.$parent.onImport = onImport;
    scope.$parent.onExport = onExport;
    scope.$parent.onRefresh = function(){
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
    };

    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        $('#filterEmployee .zb-open-modal').click();
    };

    scope.addEmail = function(val){
        if(val && val.length > 0){
            services.api("${get_api_key('app_main.api.TM_EmailHR/check_using_dept')}")
                    .data(_.pluck(val, "employee_code"))
                    .done()
                    .then(function (res) {
                        if(res.exist){
                            //Tùy chọn thêm
                            $msg.confirm("${get_global_res('Notification','Thông báo')}", msgConfirm1 + "\n" + msgConfirm2, 
                            function (val) {
                                services.api("${get_api_key('app_main.api.TM_EmailHR/insert_force')}")
                                .data(scope.list_emp)
                                .done()
                                .then(function (res) {
                                    if (res.error == null) {
                                        reloadData();
                                    }
                                });
                            }).deny(function(){
                                services.api("${get_api_key('app_main.api.TM_EmailHR/insert')}")
                                .data(scope.list_emp)
                                .done()
                                .then(function (res) {
                                    if (res.error == null) {
                                        reloadData();
                                    }
                                });
                            });
                        }else{
                            //Thêm bình thường
                            services.api("${get_api_key('app_main.api.TM_EmailHR/insert_force')}")
                            .data(scope.list_emp)
                            .done()
                            .then(function (res) {
                                if (res.error == null) {
                                    reloadData();
                                }
                            });
                        }
                    })
        }
    }

    function reloadData(){
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
        scope.$$table.currentItem = null;
        scope.$$table.selectedItems = [];
        scope.list_emp = [];
        scope.$applyAsync();
    }

    function onEdit() {
        if (Object.keys(scope.$$table.currentItem).length > 0) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_global_res('detail','Chi tiết')}" , 'HRListConfiguration/form/addEmailByCompany', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TM_EmailHR/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        }
                    })
            });
        }
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TM_EmailHR'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
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
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.TM_EmailHR/get_list_email_by_company')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
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
                        scope.currentItem = null;
                        scope.$apply();
                    }
                })
    }

    (function _getDataInitCombobox() {
            scope.$root.$getInitComboboxData(scope,
                {
                    "key": "${encryptor.get_key('perf_cbb_employees_display_name_code_email')}",
                    "code": null,
                    "alias": "$$$list_emp"
                }
            );
    })();
});