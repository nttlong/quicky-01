﻿﻿(function (scope) {
    scope.__tableSource = [];
    scope.mode = 0;
    //scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    //scope.mapName = [];
    scope.$display = {
        showDetail: false,
        mapName: [],
        selectedFunction: "",
        selectFunc: function (event, f) {
            scope.$display.selectedFunction = f;
        },
    };

    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }

    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "full_name", "title": "${get_res('full_name_table_header','Họ và tên')}" },
        { "data": "employee_code", "title": "${get_res('employee_code_table_header','Mã nhân viên')}" },
        { "data": "gender", "title": "${get_res('gender_table_header','Giới tính')}" },
        { "data": "job_w_code", "title": "${get_res('job_w_code_table_header','Chức danh công việc')}" },
        { "data": "department_name", "title": "${get_res('department_name_table_header','Bộ phận')}" },
        { "data": "active", "title": "Active", "format": "checkbox", "className": "text-center" },
        { "data": "join_date", "title": "${get_res('join_date_table_header','Ngày vào làm')}", "className": "text-center" , "format": "date:" + scope.$root.systemConfig.date_format }
    ];
    scope.$$tableConfig = {};
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.$root.$commons = {
            $current_employee_code: $row.employee_code,
            $active: $row.active,
            $info_employee: {}
        };
        _getEmployee(scope.$root.$commons.$current_employee_code, function(res){
            scope.$root.$commons.$info_employee = res;
        })
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.$display.showDetail = scope.$display.showDetail === false ? true : false;
            scope.mode = 2;
            scope.$partialpage = scope.$display.mapName[0].url;

            scope.$applyAsync();
            $(window).trigger('resize');
        }, 500);
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };

    /* Tree */
    scope.treeCurrentNode = {};
    scope.treeSelectedNodes = [];
    scope.treeSelectedRootNodes = [];
    scope.treeCheckAll = false;
    scope.treeSearchText = '';
    scope.treeDisable = false;
    scope.treeMultiSelect = false;
    scope.treeMode = 3; // Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
    var _treeDepartmentsDataSource = null;
    scope.treeDepartmentsDataSource = null;

    //selectbox datasource
    scope.cbbGender = [];
    scope.cbbEmployeeActive = [];
    scope.cbbCulture = [];
    scope.cbbRetrain = [];
    scope.cbbTrainLevel = [];
    scope.cbbLabourType = [];
    scope.cbbLevelManagement = [];
    scope.cbbWorkingType = [];

    //navigation button
    scope.firstRow = firstRow;
    scope.previousRow = previousRow;
    scope.nextRow = nextRow;
    scope.lastRow = lastRow;

    //function button
    scope.addEmployee = addEmployee;
    scope.refresh = refresh;

    //Navigation: quay trở về UI list
    scope.backPage = backPage;

    //event nhấn vào tên nhân viên trên breabcumb
    scope.openFilterEmployee = function(){
        var frm = lv.FormSearch(scope, "$$$perf_cbb_employees");
        frm.EmployeeFilter(scope.$root.$commons, "$current_employee_code", "${get_res('job_w_change','CDCV có thể thuyên chuyển')}", false);
        frm.openDialog;
        frm.accept(function () {
            _getEmployee(scope.$root.$commons.$current_employee_code, function(res){
                scope.$root.$commons.$info_employee = res;
            })
        });
        frm.cancel(function () {
        });
    };

    scope.objFilterActive = {
        $$$filter_active: "2"
    }

    function _getEmployee(empCode, callback) {
        services.api("${get_api_key('app_main.api.HCSEM_Employees/get_employee_by_emp_code')}")
            .data({
                "employee_code": empCode
            })
            .done()
            .then(function (res) {
                callback(res);
            })
    }

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.$display.showDetail = scope.$display.showDetail === false ? true : false;
            scope.mode = 0;
            scope.$partialpage = scope.$display.mapName[0].url;
            scope.$display.selectedFunction = scope.$display.mapName[0].function_id;
            $(window).trigger('resize');
        }, 500);
    }

    function addEmployee() {
        $('.hcs-profile-list').fadeToggle();
        scope.$root.$commons = {
            $current_employee_code: null,
            $active: true
        };

        setTimeout(function () {
            scope.$display.showDetail = scope.$display.showDetail === false ? true : false;
            scope.mode = 1;
            scope.currentItem = {};
            scope.$partialpage = scope.$display.mapName[0].url;

            $(window).trigger('resize');
        }, 500);
    }

    function refresh() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
    }

    function firstRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.findEmployeeInDataSource(0);
            scope.$root.$commons.$info_employee = scope.__tableSource[0];
            scope.$applyAsync();
        }
    }

    function previousRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === 0 ? scope.__tableSource.length - 1 : idx_item - 1;
            scope.currentItem = scope.findEmployeeInDataSource(index);
            scope.$root.$commons.$info_employee = scope.__tableSource[index];
            scope.$applyAsync();
        }
    }

    function nextRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === (scope.__tableSource.length - 1) ? 0 : idx_item + 1;
            scope.currentItem = scope.findEmployeeInDataSource(index);
            scope.$root.$commons.$info_employee = scope.__tableSource[index];
            scope.$applyAsync();
        }
    }

    function lastRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.findEmployeeInDataSource(scope.__tableSource.length - 1);
            scope.$root.$commons.$info_employee = scope.__tableSource[scope.__tableSource.length - 1];
            scope.$applyAsync();
        }
    }

    function tableFields() {
        return [
            { "data": "full_name", "title": "${get_res('full_name_table_header','Họ và tên')}" },
            { "data": "employee_code", "title": "${get_res('employee_code_table_header','Mã nhân viên')}" },
            { "data": "gender", "title": "${get_res('gender_table_header','Giới tính')}" },
            { "data": "job_w_code", "title": "${get_res('job_w_code_table_header','Chức danh công việc')}" },
            { "data": "department_name", "title": "${get_res('department_name_table_header','Bộ phận')}" },
            { "data": "join_date", "title": "${get_res('join_date_table_header','Ngày vào làm')}", "format": "date:" + scope.$root.systemConfig.date_format }
        ];
    }

    function onSelectTableRow($row) {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.$display.showDetail = scope.$display.showDetail === false ? true : false;

            $(window).trigger('resize');
        }, 500);
    };

    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.$display = {
            mapName: []
        }

        this.$display.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

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

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        if (scope.treeCurrentNode.hasOwnProperty('department_code')) {
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.HCSEM_Employees/get_list_with_searchtext')}")
                    .data({
                        //parameter at here
                        "pageIndex": iPage - 1,
                        "pageSize": iPageLength,
                        "search": searchText,
                        "where": {
                            'department_code': scope.treeCurrentNode.department_code,
                            'active': scope.objFilterActive.$$$filter_active
                        },
                        "sort": sort,
                        'active': scope.objFilterActive.$$$filter_active
                    })
                    .done()
                    .then(function (res) {
                        var data = {
                            recordsTotal: res.total_items,
                            recordsFiltered: res.total_items,
                            data: res.items
                        };
                        console.log(11112, scope.cbbEmployeeActive)
                        scope.__tableSource = JSON.parse(JSON.stringify(res.items));
                        callback(data);
                        scope.currentItem = null;
                        scope.$apply();
                    })
        }
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }
    }

    function _departments() {
        services.api("${get_api_key('app_main.api.HCSSYS_Departments/get_list')}")
            .data()
            .done()
            .then(function (res) {
                _treeDepartmentsDataSource = res;
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                scope.$applyAsync();
            })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }
    scope.$watch('objFilterActive.$$$filter_active', function (val) {
        //alert(val)
        //scope.objFilterActive.$$$filter_active = val;
        //scope.$applyAsync();
        scope.refresh();
    });
    function _selectBoxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                    "LGender",
                    "LEmployeeActive",
                    "LCulture",
                    "LRetrain",
                    "LTrainLevel",
                    "LLevelManagement",
                    "LWorkingType",
                    "LLabourType"
                ]
            })
            .done()
            .then(function (res) {
                scope.cbbGender = getValue(res.values, "LGender");
                scope.cbbEmployeeActive = getValue(res.values, "LEmployeeActive");
                scope.cbbCulture = getValue(res.values, "LCulture");
                scope.cbbRetrain = getValue(res.values, "LRetrain");
                scope.cbbTrainLevel = getValue(res.values, "LTrainLevel");
                scope.cbbLabourType = getValue(res.values, "LLabourType");
                scope.cbbLevelManagement = getValue(res.values, "LLevelManagement");
                scope.cbbWorkingType = getValue(res.values, "LWorkingType");
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
    }

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope,
            [{
                "key": "${encryptor.get_key('perf_cbb_employees')}",
                "code": null,
                "alias": "$$$perf_cbb_employees"
            }
            ]
        );
    };

    function reloadTableData(){
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText);
    }

    (function _init_() {
        _departments();
        _selectBoxData();
        _getDataInitCombobox();
        scope.handleData = new handleData();
        scope.$display.mapName = scope.handleData.$display.mapName;
        scope.currentFunction = scope.$display.mapName[0];
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        scope.$display.selectedFunction = (scope.$display.mapName.length > 0) ? scope.$display.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("$display.selectedFunction", function (function_id) {
        var $his = scope.$root.$history.data();
        if (scope.currentItem) {
            var func = _.filter(scope.$display.mapName, function (f) {
                return f["function_id"] == function_id;
            });
            if (func.length > 0) {
                scope.$partialpage = func[0].url;
                scope.currentFunction = func[0];
            }
        }
        //window.location.href = "#page=" + $his.page + "&f=" + function_id;
    });

    //scope.$root.$history.onChange(scope, function (data) {
    //    if (scope.mapName.length > 0) {
    //        if (data.f) {
    //            scope.$partialpage = _.filter(scope.$root.$functions, function (f) {
    //                return f.function_id = data.f
    //            })[0].url;
    //            var func = _.filter(scope.mapName, function (f) {
    //                return f["function_id"] == data.f;
    //            });
    //            if (func.length > 0) {
    //                scope.$partialpage = func[0].url;
    //                scope.currentFunction = func[0];
    //            } else {
    //                window.location.href = "#";
    //            }
    //        } else {
    //            //scope.$partialpage = scope.mapName[0].url;
    //        }
    //        scope.$apply();
    //    } else {
    //        window.location.href = "#";
    //    }
    //});

    scope.$watch('treeCurrentNode', function (val) {
        reloadTableData();
    })


});