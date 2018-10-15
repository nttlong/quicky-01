(function (scope) {
    scope.mode = [0, 0];
    scope.$$table = [
        {
            tableFields: [
                { "data": "com_level_code", "title": "${get_global_res('code','Mã')}", "className": "text-center" },
                { "data": "com_level_name", "title": "${get_global_res('name','Tên')}", "className": "text-left" },
                { "data": "score_from", "title": "${get_res('apr_form_type_table_header','Hình thức đánh giá')}", "className": "text-right" },
                { "data": "score_to", "title": "${get_res('point_scale_type_table_header','Thang điểm')}", "className": "text-right" }
            ],
            $$tableConfig: {},
            tableSource: function (fnReloadData, iPage, iPageLength, orderBy, searchText) {
                scope.$$table[0].$$tableConfig = {
                    fnReloadData: fnReloadData,
                    iPage: iPage,
                    iPageLength: iPageLength,
                    orderBy: orderBy,
                    searchText: searchText
                };
                if (fnReloadData) {
                    if (searchText) {
                        _loadLevel(iPage, iPageLength, orderBy, searchText, function (data) {
                            fnReloadData(data);
                        });
                    } else {
                        _loadLevel(iPage, iPageLength, orderBy, null, function (data) {
                            fnReloadData(data);
                        });
                    }
                }
            },
            onSelectTableRow: function ($row) { scope.event[0].edit(); },
            selectedItems: [],
            currentItem: {},
            tableSearchText: "",
            refreshDataRow: function () { /*Do nothing*/ }
        },
        {
            tableFields: [
                { "data": "action", "title": "${get_res('action','Hành động tiêu chuẩn')}", "className": "text-left" },
                { "data": "weight", "title": "${get_global_res('weight','Trọng số')}", "className": "text-left" }
            ],
            $$tableConfig: {},
            tableSource: function (fnReloadData, iPage, iPageLength, orderBy, searchText) {
                scope.$$table[1].$$tableConfig = {
                    fnReloadData: fnReloadData,
                    iPage: iPage,
                    iPageLength: iPageLength,
                    orderBy: orderBy,
                    searchText: searchText
                };
                if (fnReloadData) {
                    if (searchText) {
                        _loadAction(iPage, iPageLength, orderBy, searchText, function (data) {
                            fnReloadData(data);
                        });
                    } else {
                        _loadAction(iPage, iPageLength, orderBy, null, function (data) {
                            fnReloadData(data);
                        });
                    }
                }
            },
            onSelectTableRow: function ($row) { scope.event[1].edit(); },
            selectedItems: [],
            currentItem: {},
            tableSearchText: "",
            refreshDataRow: function () { /*Do nothing*/ }
        }
    ];

    scope.event = [{
        add: function () {
            scope.mode[0] = 1;
            openDialog("${get_res('detail_level','Chi tiết cấp độ')}",
                'competencyDictionary/form/Competency/level/addLevel',
                function () { }, "addLevel");
        },
        edit: function () {
            if (Object.keys(scope.$$table[0].currentItem).length > 0) {
                scope.mode[0] = 2;
                openDialog("${get_res('detail_level','Chi tiết cấp độ')}",
                    'competencyDictionary/form/Competency/level/addLevel',
                    function () { }, "addLevel");
            } else {
                $msg.message("${get_global_res('Notification','Thông báo')}",
                    "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
        },
        delete: function () {
            if (scope.$$table[0].selectedItems.length == 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
            else {
                var param = {
                    "com_level_code":_.pluck(scope.$$table[0].selectedItems, 'com_level_code'),
                    "com_code": scope.$parent.$com_code
                };
                //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}" + "\n" +
                    "${get_global_res('the_operation_can_delete_standard_behavior_by_level','Thao tác này có thể sẽ xóa hành vi tiêu chuẩn theo cấp độ')}" + ".", function () {
                    services.api("${get_api_key('app_main.api.TMLS_CompetencyLevel/delete')}")
                        .data(param)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                _loadLevel(scope.$$table[0].$$tableConfig.iPage, scope.$$table[0].$$tableConfig.iPageLength, 
                                        scope.$$table[0].$$tableConfig.orderBy, scope.$$table[0].$$tableConfig.searchText, 
                                        scope.$$table[0].$$tableConfig.fnReloadData);
                                _loadAction(scope.$$table[1].$$tableConfig.iPage, scope.$$table[1].$$tableConfig.iPageLength, 
                                        scope.$$table[1].$$tableConfig.orderBy, scope.$$table[1].$$tableConfig.searchText, 
                                        scope.$$table[1].$$tableConfig.fnReloadData);
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                            }
                            else if (res['error'] == "CompetencyGroup is using another PG") {
                                $msg.alert("${get_global_res('node_selected_use_other_process','Nút được chọn đang được sử dụng bởi xử lí khác')}", $type_alert.INFO);
                            }
                            else {
                                $msg.alert("${get_global_res('Handle_failed','Thao tác thất bại')}", $type_alert.DANGER);
                            }
                        });
                });
            }
         },
        refresh: function () { 
            _loadLevel(scope.$$table[0].$$tableConfig.iPage, scope.$$table[0].$$tableConfig.iPageLength, 
                        scope.$$table[0].$$tableConfig.orderBy, scope.$$table[0].$$tableConfig.searchText, 
                        scope.$$table[0].$$tableConfig.fnReloadData);
        }
    },
    {
        add: function () {
            if(Object.keys(scope.$$table[0].currentItem).length > 0){
                scope.mode[1] = 1;
                openDialog("${get_res('detail_standard_action','Chi tiết hành vi tiêu chuẩn')}",
                    'competencyDictionary/form/Competency/level/addAction',
                    function () { }, "addAction");
            }else{
                $msg.message("${get_global_res('Notification','Thông báo')}",
                    "${get_res('you_need_select_parent_level_before_add_action','Cần chọn cấp độ trước khi tạo mới hành động')}", function(){});
            }
        },
        edit: function () {
            if (Object.keys(scope.$$table[1].currentItem).length > 0) {
                scope.mode[1] = 2;
                openDialog("${get_res('detail_standard_action','Chi tiết hành vi tiêu chuẩn')}",
                    'competencyDictionary/form/Competency/level/addAction',
                    function () { }, "addAction");
            } else {
                $msg.message("${get_global_res('Notification','Thông báo')}",
                    "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
        },
        delete: function () { 
            if (scope.$$table[1].selectedItems.length == 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
            else {
                var param = {
                    "com_level_code": scope.$$table[0].currentItem['com_level_code'],
                    "com_code": scope.$parent.$com_code,
                    "_id": _.pluck(scope.$$table[1].selectedItems, '_id')
                };
                //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                    services.api("${get_api_key('app_main.api.TMLS_CompetencyAction/delete')}")
                        .data(param)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                _loadAction(scope.$$table[1].$$tableConfig.iPage, scope.$$table[1].$$tableConfig.iPageLength, 
                                        scope.$$table[1].$$tableConfig.orderBy, scope.$$table[1].$$tableConfig.searchText, 
                                        scope.$$table[1].$$tableConfig.fnReloadData);
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                            }
                            else if (res['error'] == "CompetencyGroup is using another PG") {
                                $msg.alert("${get_global_res('node_selected_use_other_process','Nút được chọn đang được sử dụng bởi xử lí khác')}", $type_alert.INFO);
                            }
                            else {
                                $msg.alert("${get_global_res('Handle_failed','Thao tác thất bại')}", $type_alert.DANGER);
                            }
                        });
                });
            }
        },
        refresh: function () { 
            _loadAction(scope.$$table[1].$$tableConfig.iPage, scope.$$table[1].$$tableConfig.iPageLength, 
                        scope.$$table[1].$$tableConfig.orderBy, scope.$$table[1].$$tableConfig.searchText, 
                        scope.$$table[1].$$tableConfig.fnReloadData);
        }
    }];

    scope._loadLevel = _loadLevel;
    scope._loadAction = _loadAction;

    function _loadLevel(iPage, iPageLength, orderBy, searchText, callback) {
        if(scope.$parent.$com_code){
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.TMLS_CompetencyLevel/get_list_with_searchtext')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "com_code": scope.$parent.$com_code
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
    }

    function _loadAction(iPage, iPageLength, orderBy, searchText, callback) {
        if(scope.$$table[0].currentItem && Object.keys(scope.$$table[0].currentItem).length > 0){
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.TMLS_CompetencyAction/get_list_with_searchtext')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "sort": sort,
                        "level": scope.$$table[0].currentItem['com_level_code'],
                        "com_code": scope.$parent.$com_code
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
    }

    function openDialog(title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    scope.onSearchTable0 = function(val){
        scope.$$table[0].tableSearchText = val;
        scope.$apply();
    }

    scope.onSearchTable1 = function(val){
        scope.$$table[1].tableSearchText = val;
        scope.$apply();
    }

    scope.$watch('$$table[0].currentItem', function(val){
        if(val && Object.keys(val).length > 0){
            _loadAction(scope.$$table[1].$$tableConfig.iPage, scope.$$table[1].$$tableConfig.iPageLength, 
            scope.$$table[1].$$tableConfig.orderBy, scope.$$table[1].$$tableConfig.searchText, 
            scope.$$table[1].$$tableConfig.fnReloadData)
        }
    })
});