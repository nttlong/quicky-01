(function (scope) {
    var _default = {
        _id : null,
        com_code:scope.$parent.$com_code,
        factor:"",
        weight:"",
        com_level_code:"",
        ordinal:""
    }

    scope.mode = 1;

    scope.$$table = {
        tableFields: [
            { "data": "factor", "title": "${get_res('factor_table_header','Yếu tố đánh giá')}" },
            { "data": "weight", "title": "${get_res('weight_table_header','Trọng số')}" },
            { "data": "com_level_code", "title": "${get_res('com_level_code_table_header','Dành cho cấp độ')}" }
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
            services.api("${get_api_key('app_main.api.TMLS_CompetencyFactor/get_list_with_searchtext')}")
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
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.$$table.currentItem = null;
                    scope.$apply();
                })
    }

    scope.event = {
        add : function(){
            scope.mode = 1;
            scope.entity = null;
            scope.$applyAsync();
        },
        delete: function(){
            if (scope.$$table.selectedItems.length == 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
            else {
                var param = {
                    "com_code": scope.$parent.$com_code,
                    "_id": _.pluck(scope.$$table.selectedItems, '_id')
                };
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                    services.api("${get_api_key('app_main.api.TMLS_CompetencyFactor/delete')}")
                        .data(param)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                scope.event.refresh();
                                scope.event.add();
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                            }
                            else {
                                $msg.alert("${get_global_res('Handle_failed','Thao tác thất bại')}", $type_alert.DANGER);
                            }
                        });
                });
            }
        },
        refresh: function(){
            var config = scope.$$table.$$tableConfig;
            _tableData(config.iPage, config.iPageLength, config.orderBy, config.searchText, config.fnReloadData);
        },
        save: function(){
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Save','Bạn có muốn lưu không?')}", function () {
                if (scope.entity != null) {
                    var rsCheck = checkError();
                    if (rsCheck.result) {
                        $msg.message("${get_global_res('Input_Error','Nhập liệu sai')}", rsCheck.errorMsg, function () { });
                        return;
                    }
                    editData(function (res) {
                        if (res.error == null) {
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.event.refresh();
                            scope.event.add();
                            scope.$applyAsync();
                        } else {
                            $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                        }
                    });
                }
            });
        }
    }

    scope.onSearch = function(val){
        scope.$$table.$$tableConfig.searchText = val;
        scope.event.refresh();
    }

    function checkError() {
        var errMsg;
        var valid = null;
        var rs = {
            "result": false,
            "errorMsg": ''
        };
        valid = lv.Validate(scope.entity.factor);
        rs.result = valid.isNullOrWhiteSpace();
        rs.errorMsg = rs.result === true ? "${get_res('factor_is_not_null','Yếu tố đánh giá được để trống')}" + '\n' : "";
        if (rs.result === true) {
            return rs;
        }
        return rs;
    }

    function editData(callback) {
        var url = getUrl();
        var param = _.mapObject(_default, function(val, key) { return val = scope.entity[key] ? scope.entity[key] : null });
        param['com_code'] = scope.$parent.$com_code;
        services.api(url)
            .data(param)
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function getUrl() {
        return scope.mode == 1 || scope.mode == 3 ? "${get_api_key('app_main.api.TMLS_CompetencyFactor/insert')}"
            : "${get_api_key('app_main.api.TMLS_CompetencyFactor/update')}"
    }

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            {
                "key": "${encryptor.get_key('cbb_com_level_group_by_com_code')}",
                "code": scope.entity
                    && scope.entity.hasOwnProperty('com_level_code')
                    ? scope.entity.com_level_code
                    : null,
                "alias": "$$$cbb_com_level_group_by_com_code",
                "predicate": [{ "@com_code":scope.$parent.$com_code}],
            }
        );
    };

    _getDataInitCombobox();

    scope.$watch("$$table.currentItem", function(val){
        if(val && Object.keys(val).length > 0){
            scope.mode = 2;
            scope.entity = JSON.parse(angular.toJson(val));
            _getDataInitCombobox();
        }
    })
});