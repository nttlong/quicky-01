(function (scope) {
    scope.mode = 0;   
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.obj = {
        showDetail: false,
        selectedFunction: "",
        selectFunc: function (event, f) {
            scope.detail.selectedFunction = f;
        },
    }
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    scope.SearchText = '';
    scope._reloadData = _reloadData;
    /* Table */
    scope.$$table = {
        tableFields: [
            { "data": "process_id", "title": "${get_res('process_id','Mã quy trình')}", "className": "text-center" },
            { "data": "process_name", "title": "${get_res('process_name','Tên quy trình')}", "className": "text-left" },
            { "data": "max_approve_level", "title": "${get_res('max_approve_level','Số cấp duyệt')}", "className": "text-center" }
            //,{ "data": "created_on", "title": "${get_res('created_on','Ngày tạo')}", "className": "text-center" }

        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) {
            scope.button.edit();
        },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    scope.button = {
        add: function () {
            scope.mode = 1;
            redirectPage();
        },
        edit: function () {
            scope.mode = 2;
            redirectPage();
        },
        delete: function () {
            if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            } else {
                $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                    services.api("${get_api_key('app_main.api.HCSSYS_Departments/delete')}")
                        .data(scope.$$table.selectedItems)
                        .done()
                        .then(function (res) {
                            if (res.deleted > 0) {
                                _reloadData();
                                $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                                scope.$$table.currentItem = null;
                                scope.$$table.selectedItems = [];
                            } else if (res.error !== null || res.error !== "") {
                                $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_is_using','CDCV đang được sử dụng')}", function () { });
                            }
                        })
                });
            }
        },
        refresh: function () {
            _reloadData();
        }
    }

    //Navigation: quay trở về UI list
    scope.backPage = backPage;

    function redirectPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.obj.showDetail = scope.obj.showDetail === false ? true : false;
            scope.$partialpage = scope.mapName[0].url;
            $(window).trigger('resize');
        }, 300);
    }

    function _reloadData() {
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy,
            config.searchText, config.fnReloadData)
    }

    function onSelectedRow($row) {
        scope.mode = 2;
        redirectPage();
    }

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.obj.showDetail = scope.obj.showDetail === false ? true : false;
            scope.mode = 0;
            scope.$partialpage = scope.mapName[0].url;
            scope.obj.selectedFunction = scope.mapName[0].function_id;
            $(window).trigger('resize');
        }, 400);
    }

    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName =
            [{
                default_name: "${get_global_res('config_general','Thiết lập chung')}",
                custom_name: "${get_global_res('config_general','Thiết lập chung')}",
                url: "setup_process/setup_process_detail/setup_process_general",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "1",
                active: true,
                function_id: "LMSLS_HTQT0041"
            },
            {
                default_name: "${get_global_res('config_detail','Cấp duyệt chi tiết')}",
                custom_name: "${get_global_res('config_detail','Cấp duyệt chi tiết')}",
                url: "setup_process/setup_process_detail/setup_process_approve_level",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "2",
                active: true,
                function_id: "LMSLS_HTQT0042"
            },
            {
                default_name: "${get_global_res('config_default','Cấp duyệt mặc định')}",
                custom_name: "${get_global_res('config_default','Cấp duyệt mặc định')}",
                url: "setup_process/setup_process_detail/setup_process_approve_level_default",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "3",
                active: true,
                function_id: "LMSLS_HTQT0043"
            },
            {
                default_name: "${get_global_res('approve_dept','Duyệt theo bộ phận')}",
                custom_name: "${get_global_res('approve_dept','Duyệt theo bộ phận')}",
                url: "setup_process/setup_process_detail/setup_process_approve_dept",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "4",
                active: true,
                function_id: "LMSLS_HTQT0044"
            },
            {
                default_name: "${get_global_res('approve_emp','Duyệt theo nhân viên')}",
                custom_name: "${get_global_res('approve_emp','Duyệt theo nhân viên')}",
                url: "setup_process/setup_process_detail/setup_process_approve_emp",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "5",
                active: true,
                function_id: "LMSLS_HTQT0045"
            },
            {
                default_name: "${get_global_res('approve_emp','Uỷ quyền duyệt thay')}",
                custom_name: "${get_global_res('approve_emp','Uỷ quyền duyệt thay')}",
                url: "setup_process/setup_process_detail/setup_process_approve_substitute",
                icon: "bowtie-icon bowtie-edit-copy",
                sorting: "6",
                active: true,
                function_id: "LMSLS_HTQT0046"
            }
            ];
        //_.filter(scope.$root.$function_list, function (f) {
        //return f.level_code.includes(scope.$root.currentFunction.function_id)
        //    && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        //});

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

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
            services.api("${get_api_key('app_main.api.LMS_SetupProcess/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
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
                    scope.$apply();
                })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }

    (function _init_() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.$partialpage = scope.mapName[0].url;
        scope.currentFunction = scope.mapName[0];
        scope.obj.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("obj.selectedFunction", function (function_id) {
        var $his = scope.$root.$history.data();
        if (scope.$$table.currentItem) {
            var func = _.filter(scope.mapName, function (f) {
                return f["function_id"] == function_id;
            });
            if (func.length > 0) {
                scope.$partialpage = func[0].url;
                scope.currentFunction = func[0];
            }
        }
    });

});
