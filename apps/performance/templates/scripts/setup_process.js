(function (scope) {
    scope.mode = 0;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.currentSetupProcess = null;
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
            scope.currentProcess = $row;
            scope.button.edit($row);
        },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    scope.$$process_id = null;
    scope.$$is_approve_by_dept = null;

    scope.button = {
        add: function () {
            scope.mode = 1;
            redirectPage();
        },
        edit: function ($row) {
            debugger
            scope.mode = 2;
            _init_($row.process_id);
            scope.$$process_id = scope.$$table.currentItem.process_id;
            scope.$$curr_max_approve_level = scope.$$table.currentItem.max_approve_level;
            scope.$$is_approve_by_dept = scope.$$table.currentItem.is_approve_by_dept;
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
        //$('.hcs-profile-list').fadeToggle();
        //setTimeout(function () {
            scope.obj.showDetail = scope.obj.showDetail === false ? true : false;
            scope.mode = 0;
            scope.$partialpage = scope.mapName[0].url;
            scope.obj.selectedFunction = scope.mapName[0].function_id;
            $(window).trigger('resize');
        // }, 100);
    }

    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName ={
                    "DauKy": [
                        {
                            default_name: "${get_global_res('config_general','Thiết lập chung')}",
                            custom_name: "${get_global_res('config_general','Thiết lập chung')}",
                            url: "setup_process/setup_process_detail/setup_process_general",
                            icon: "bowtie-icon bowtie-settings-gear-outline",
                            sorting: "1",
                            active: true,
                            function_id: "TMSYS0011"
                        },
                        {
                            default_name: "${get_global_res('config_details','Cấp duyệt')}",
                            custom_name: "${get_global_res('config_details','Cấp duyệt')}",
                            url: "setup_process/setup_process_detail/setup_process_approve_level",
                            icon: "bowtie-icon bowtie-step",
                            sorting: "2",
                            active: true,
                            function_id: "TMSYS0012"
                        },
                        {
                            default_name: "${get_global_res('config_defaults','Người duyệt')}",
                            custom_name: "${get_global_res('config_defaults','Người duyệt')}",
                            url: "setup_process/setup_process_detail/setup_process_approve_emp",
                            sorting: "3",
                            icon: "la la-user-plus",
                            active: true,
                            function_id: "TMSYS0013"
                        },
                        {
                            default_name: "${get_global_res('approve_substitute','Uỷ quyền')}",
                            custom_name: "${get_global_res('approve_substitute','Uỷ quyền')}",
                            url: "setup_process/setup_process_detail/setup_process_approve_substitute",
                            icon: "bowtie-icon bowtie-security-group",
                            sorting: "4",
                            active: true,
                            function_id: "TMSYS0014"
                        }
                    ],
                    "CuoiKy": [
                        {
                            default_name: "${get_global_res('config_general','Thiết lập chung')}",
                            custom_name: "${get_global_res('config_general','Thiết lập chung')}",
                            url: "setup_process/setup_process_detail_last/setup_process_general",
                            icon: "bowtie-icon bowtie-settings-gear-outline",
                            sorting: "1",
                            active: true,
                            function_id: "TMSYS0021"
                        },
                        {
                            default_name: "${get_global_res('config_details','Cấp duyệt')}",
                            custom_name: "${get_global_res('config_details','Cấp duyệt')}",
                            url: "setup_process/setup_process_detail_last/setup_process_approve_level",
                            icon: "bowtie-icon bowtie-step",
                            sorting: "2",
                            active: true,
                            function_id: "TMSYS0022"
                        },
                        {
                            default_name: "${get_res('use_for_employee','Dùng cho nhân viên')}",
                            custom_name: "${get_res('use_for_employee','Dùng cho nhân viên')}",
                            url: "setup_process/setup_process_detail_last/setup_process_employee",
                            icon: "fa fa-user",
                            sorting: "4",
                            active: true,
                            function_id: "TMSYS0023"
                        },
                        {
                            default_name: "${get_global_res('config_defaults','Người duyệt')}",
                            custom_name: "${get_global_res('config_defaults','Người duyệt')}",
                            url: "setup_process/setup_process_detail_last/setup_process_approve_emp",
                            icon: "la la-user-plus",
                            sorting: "3",
                            active: true,
                            function_id: "TMSYS0024"
                        },
                        {
                            default_name: "${get_global_res('approve_substitute','Uỷ quyền')}",
                            custom_name: "${get_global_res('approve_substitute','Uỷ quyền')}",
                            url: "setup_process/setup_process_detail_last/setup_process_approve_substitute",
                            icon: "bowtie-icon bowtie-security-group",
                            sorting: "4",
                            active: true,
                            function_id: "TMSYS0025"
                        }
                    ]
            };
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
            services.api("${get_api_key('app_main.api.TM_SetupProcess/get_list_with_searchtext')}")
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

    function _init_(process_id) {
        scope.handleData = new handleData();
        switch(process_id){
            case "1":
                scope.mapName = scope.handleData.mapName["DauKy"];break;
            case "2":
                scope.mapName = scope.handleData.mapName["CuoiKy"];break;
        }
        scope.$partialpage = scope.mapName[0].url;
        scope.currentFunction = scope.mapName[0];
        scope.obj.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        scope.$applyAsync();
    };

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
