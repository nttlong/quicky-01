﻿(function (scope) {
    //("===============BEGIN TABLE==================")
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "rank_code", "title": "${get_res('rank_code_table_header','Mã')}", "className": "text-left" },
        { "data": "rank_name", "title": "${get_res('rank_name_table_header','Tên')}", "className": "text-left" },
        { "data": "rank_content", "title": "${get_res('rank_content_table_header','Đánh giá chung')}", "className": "text-left" },
        { "data": "total_from", "title": "${get_res('total_from_table_header','Tổng điểm từ')}","format":"number: system", "className": "text-left" },
        { "data": "total_to", "title": "${get_res('total_to_table_header','Tổng điểm đến')}","format":"number: system", "className": "text-left" },
        { "data": "is_change_object", "title": "${get_res('is_change_object_table_header','Thiết lập riêng')}", "className": "text-center", "format": "checkbox" },
        { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}","format":"number: system", "className": "text-center" },
        { "data": "lock", "title": "${get_res('lock_table_header','Ngưng SD')}", "className": "text-center", "format": "checkbox" }
    ];
    //
    scope.$$tableConfig = {};
    scope.currFunction = "HCSSYS0020";
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
    scope.onRefresh = onRefresh;
    scope.onCopy = onCopy;
    scope.onSearch = onSearch;
    scope.onExport = onExport;
    scope.onImport = onImport;
    // scope.$parent.onEdit = onEdit;
    // scope.$parent.onAdd = onAdd;
    // scope.$parent.onDelete = onDelete;
    // scope.$parent.onCopy = onCopy;
    // scope.$parent.onSearch = onSearch;
    // scope.$parent.onExport = onExport;
    // scope.$parent.onImport = onImport;
    scope._tableData = _tableData;
    scope.cbbContinents = [];
    //scope.getDisplayNameAccessMode = getDisplayNameAccessMode;

    function onRefresh(){
        var config = scope.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    }

    /**
     * Hàm mở form chỉnh sửa
     */
    function onEdit() {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_Rank_Personal','Chi tiết xếp loại cá nhân')}", 'rankcategory/form/addPersonal', function () {
                //$(window).trigger('resize');
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_Rank_Personal','Chi tiết xếp loại cá nhân')}", 'rankcategory/form/addPersonal', function () {
            //$(window).trigger('resize');
        });
    }
    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_Rank/delete')}")
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
            openDialog("${get_res('Detail_Rank_Personal','Chi tiết xếp loại cá nhân')}", 'rankcategory/form/addPersonal', function () { });
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
                'collection_name': 'HCSLS_Nation'
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
            services.api("${get_api_key('app_main.api.TMLS_Rank/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "lock": scope.$parent.advancedSearch.data_lock,
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
    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
                "name": "LContinents"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                scope.cbbContinents = res.values;
                console.log(res);
                scope.$applyAsync();
            })
    }
    _comboboxData();

    scope.$parent.$watch("advancedSearch.data_lock", function (val) {
        var config = scope.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    });
    //("===============INIT==================")
    //_tableData();
    //("===============END TABLE==================")
});