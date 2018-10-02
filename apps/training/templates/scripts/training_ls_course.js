(function (scope) {
    /**
     * Table
     */
    scope.$$table = {
        tableFields: [
            { "data": "course_code", "title": "${get_res('course_code_table_header','Mã')}" },
            { "data": "course_name", "title": "${get_res('course_name_table_header','Tên khóa')}" },
            { "data": "course_name2", "title": "${get_res('course_name2_table_header','Tên khác')}" },
            { "data": "course_content", "title": "${get_res('course_content_table_header','Nội dung')}"},
            { "data": "method", "title": "${get_res('method_table_header','Phương thức')}" },
            //{ "data": "periodic", "title": "${get_res('periodic_table_header','Định kỳ')}" },
            { "data": "display_periodic", "title": "${get_res('periodic_table_header','Định kỳ')}" },
            { "data": "number_month", "title": "${get_res('number_month_table_header','Số tháng')}" },
            { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}" },
            { "data": "lock", "title": "${get_res('lock','Ngưng SD')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope.__tableSource = [];
    scope.__valueListCompetency = [];
    scope.CompetencyType = null;
    scope._tableData = _tableData;
    scope.mode = 0;
    scope.searchText = "";
    scope.onSelectTableRow = pressEnter;


    /* Tree */
    scope.$$tree = {
        treeCurrentNode: {},
        treeSelectedNodes: [],
        treeSelectedRootNodes: [],
        treeCheckAll: false,
        treeSearchText: '',
        treeDisable: false,
        treeMultiSelect: false,
        treeMode: 3,// Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
        treeDataSource: null
    };

    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;


    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }




    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Train_LsCourse_Detail','Chi tiết khóa đào tạo')}", 'form/addTrainLsCourse', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem && Object.keys(scope.$$table.currentItem).length > 0) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Edit_Train_LsCourse','Chi tiết khóa đào tạo')}", 'form/addTrainLsCourse', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (scope.$$table.currentItem && Object.keys(scope.$$table.currentItem).length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_TrainLsCourse/delete')}")
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

    function pressEnter($row) {
        scope.onEdit();
    }
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'HCSLS_TrainLsCourse'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }
    function onAttach() {

    };
    function onRefresh() {
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
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
    debugger
         var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSLS_TrainLsCourse/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "train_group_code": scope.$$tree.treeCurrentNode.hasOwnProperty("train_group_code") === true ? scope.$$tree.treeCurrentNode.train_group_code : null,
                    "com_type": scope.CompetencyType ? scope.CompetencyType['value'] : 0,
                    //"lock": scope.$parent.$parent.$parent.advancedSearch.data_lock
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

    function _loadTreeDataSource() {
        services.api("${get_api_key('app_main.api.HCSLS_TrainCourseGroup/get_tree')}")
            .data({
                //"lock": scope.$parent.advancedSearch.data_lock
            })
            .done()
            .then(function (res) {
                scope.$$tree.treeDataSource = res;
                scope.$applyAsync();
            })
    }


    _loadTreeDataSource();

    scope.$watch("$$tree.treeCurrentNode", function () {
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    });

    scope.$parent.$parent.$parent.$watch("advancedSearch.data_lock", function (val) {
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
    });
});