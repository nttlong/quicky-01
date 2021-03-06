(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "question_id", "title": "${get_res('id','ID')}", "className": "text-left" },
            { "data": "question_content_1", "title": "${get_res('Question','Question')}", "className": "text-left" },
            { "data": "category_type_name", "title": "${get_res('question_type','Question Type')}", "className": "text-left" },
            { "data": "total_temp_size", "title": "${get_res('assigned_to','Assigned to')}", "className": "text-left", "expr":function(row, data, func){
                func(function(){
                    return "<span>" + row.total_temp_size + "</span> <span style='color: green;' class='sap-icon sap-menu'></span>" ;

                });
                return true;
            } },
            { "data": "created_on", "title": "${get_res('created_at','Created at')}", "format": "date:" + scope.$root.systemConfig.date_format, "className": "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: '',
        refreshDataRow: function () { /*Do nothing*/ }
    };

    scope._tableData = _tableData;
    scope.searchText = "";

    scope.onAdd = onAdd;
    scope.onEdit = onEdit;
    scope.onDelete = onDelete;
    scope.onImport = onImport;
    scope.onExport = onExport;
    scope.onRefresh = onRefresh;

    scope.onSearchText = function(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
            scope.$apply();
    }

    function onAdd() {
        scope.mode = 1;
        openDialog("${get_res('add_question','Thêm câu hỏi')}", 'form/addSurQuestionBank', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2;
            openDialog("${get_res('detal_sur_question','Chi tiết câu hỏi')}" + ": " + scope.$$table.currentItem.question_content_1, 'form/addSurQuestionBank', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMS_SurQuestionBankController/delete')}")
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
                'collection_name': 'TMLS_Competency'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }
    function onRefresh() {
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    };

    function openDialog(title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    scope.reloadData = function (){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
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

    scope.$watch("groupCategory", function(v, o){
        scope.reloadData();
    })

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMS_SurQuestionBankController/get_list')}")
                .data({
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "where": {
                        category_id: scope.groupCategory ? scope.groupCategory.category_id : null
                    }
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

    function _loadValueList() {
        services.api("${get_api_key('app_main.api.LMS_SurQuestionCategoryController/get_value_list')}")
            .data({})
            .done()
            .then(function (res) {
                res.unshift({
                    "category_id" : null,
                    "category_name" : "(" + "${get_res('all','Tất cả')}" + ")"
                });
                scope.__valueList = res;
                scope.groupCategory = scope.__valueList[0];
                scope.$applyAsync();
            })
    }

    (function __init__() {
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        _loadValueList();
    })();

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
        {
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        }else{
            window.location.href = '#page=' + scope.$root.$extension.TripleDES.encrypt(data['page']);
        }
    });

    // scope.$watch("$$tree.treeCurrentNode", function (old, newVal) {
    //     if (newVal && old != newVal)
    //         _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    // });

    // scope.$parent.$watch("advancedSearch.data_lock", function (old, newVal) {
    //     if (newVal && old != newVal)
    //         _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    // });

    // scope.$watch('CompetencyType', function (old, newVal) {
    //     if (newVal && old != newVal)
    //         _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    // })

    // scope.$watch('$$table', function (val) {
    //     console.log(val);
    // })
});