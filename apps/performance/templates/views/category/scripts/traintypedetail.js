﻿(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "train_detail_code", "title": "${get_res('train_detail_code_table_header','Mã')}", "className": "text-left", width: "170px" },
        { "data": "train_detail_name", "title": "${get_res('train_detail_name_table_header','Tên')}", "className": "text-left" },
        { "data": "note", "title": "${get_res('note_table_header','Ghi chú')}", "className": "text-left" },
        { "data": "ordinal", "format":"number: system", "title": "${get_res('ordinal_table_header','Thứ tự')}", "className": "text-center", width: "100px" },
        { "data": "created_on", "title": "${get_res('created_on_table_header','Ngày tạo')}", "className": "text-left", "format": "date:" + scope.$root.systemConfig.date_format, width: "100px" },
        { "data": "lock", "title": "${get_res('lock_table_header','Ngưng SD')}", "className": "text-center", "format": "checkbox", width: "100px" },
    ];
    //
    scope.$$tableConfig = {};
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
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
    scope.onSelectTableRow = pressEnter;
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };
    //Mode 1: tạo mới, Mode 2: chỉnh sửa, Mode 3: sao chép
    scope.mode = 0;
    scope.onEdit = onEdit;
    scope.onAdd = onAdd;
    scope.onDelete = onDelete;
    scope.onCopy = onCopy;
    scope.onSearch = onSearch;
    scope.onExport = onExport;
    scope.onImport = onImport;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onCopy = onCopy;
    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onRefresh = reloadData;
    scope._tableData = _tableData;
    scope.cbbQuitJobType = [];

    function reloadData (){
        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
    }

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_TrainTypeDetail','Chi tiết Hình thức đào tạo')}", 'category/form/addTrainTypeDetail', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_TrainTypeDetail','Chi tiết Hình thức đào tạo')}", 'category/form/addTrainTypeDetail', function () { });
    }
    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_TrainTypeDetail/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    }
    function onCopy() {
        if (scope.currentItem) {
            scope.mode = 3; // set mode chỉnh sửa
            openDialog("${get_res('Detail_TrainTypeDetail','Chi tiết Hình thức đào tạo')}", 'category/form/addTrainTypeDetail', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$apply();
    }
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'HCSLS_TrainTypeDetail'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            //.setFunctionID("aaaaa")
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

    function pressEnter($row) {
        scope.onEdit();
    }

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSLS_TrainTypeDetail/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "lock": scope.$parent.$parent.advancedSearch.data_lock,
                    "sort": sort
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

    scope.$parent.$watch("advancedSearch.data_lock", function (val) {
        var config = scope.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    });
    //("===============INIT==================")
    //_tableData();
    //("===============END TABLE==================")
});