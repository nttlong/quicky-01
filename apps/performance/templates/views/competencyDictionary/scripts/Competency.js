(function (scope) {
    /**
     * Table
     */
    scope.$parent.$parent.$parent.isChangeFunc =  true;
    scope.$$table = {
        tableFields: [
            { "data": "com_code", "title": "${get_global_res('code','Mã')}", "className": "text-left" },
            { "data": "com_name", "title": "${get_global_res('name','Tên')}", "className": "text-left" },
            { "data": "apr_form_type", "title": "${get_res('apr_form_type_table_header','Hình thức đánh giá')}", "className": "text-left" },
            { "data": "point_scale_type", "title": "${get_res('point_scale_type_table_header','Thang điểm')}", "className": "text-left" },
            { "data": "ordinal", "title": "${get_res('ordinal_table_header','Thứ tự')}", "className": "text-center" },
            { "data": "lock", "title": "${get_res('lock_table_header','Toàn cty')}", "className": "text-center", "format": "checkbox" }
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
        openDialog("${get_res('detail_competency_dictionary','Chi tiết từ điển năng lực')}", 'competencyDictionary/form/addCompetency', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('detail_competency_dictionary','Chi tiết từ điển năng lực')}" + ": " + scope.$$table.currentItem.com_name, 'competencyDictionary/form/addCompetency', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}" + 
                "\n" +
                "${get_res('level_and_factor_will_be_delete','Cấp độ và yếu tố đánh giá của năng lực này sẽ được xóa theo.')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_Competency/delete')}")
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
                'collection_name': 'TMLS_Competency'
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
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.TMLS_Competency/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "com_group_code": scope.$$tree.treeCurrentNode.hasOwnProperty("com_group_code") === true ? scope.$$tree.treeCurrentNode.com_group_code : null,
                    "com_type": scope.CompetencyType ? scope.CompetencyType['value'] : 0,
                    "lock": scope.$parent.$parent.$parent.advancedSearch.data_lock
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

    function _loadTreeDataSource() {
        services.api("${get_api_key('app_main.api.TMLS_CompetencyGroup/get_tree')}")
            .data({
                "lock": scope.$parent.advancedSearch.data_lock
            })
            .done()
            .then(function (res) {
                scope.$$tree.treeDataSource = res;
                scope.$applyAsync();
            })
    }

    function _loadValueList() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": "PERF_Competency_Type"
            })
            .done()
            .then(function (res) {
                scope.__valueListCompetency = res.values;
                scope.CompetencyType = scope.__valueListCompetency[0];
                scope.$applyAsync();
            })
    }

    (function __init__() {
        _loadTreeDataSource();
        _loadValueList();
    })();

    scope.$watch("$$tree.treeCurrentNode", function (old, newVal) {
        if (newVal && old != newVal)
            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    });

    scope.$parent.$watch("advancedSearch.data_lock", function (old, newVal) {
        if (newVal && old != newVal)
            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    });

    scope.$watch('CompetencyType', function (old, newVal) {
        if (newVal && old != newVal)
            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    })

    scope.$watch('$$table', function (val) {
        console.log(val);
    })
});