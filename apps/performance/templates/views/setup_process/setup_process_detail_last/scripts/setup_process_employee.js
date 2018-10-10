(function (scope) {
    /**
     * Table
     */
    scope.$parent.$parent.$parent.isChangeFunc = true;
    scope.$$table = {
        tableFields: [
            { "data": "employee_code", "title": "${get_global_res('code','Mã')}", "className": "text-left" },
            { "data": "employee_name", "title": "${get_res('full_name','Họ và tên')}", "className": "text-left" },
            { "data": "department_name", "title": "${get_res('department','Bộ phận')}", "className": "text-left" },
            { "data": "job_w_name", "title": "${get_res('job_working','Chức danh công việc')}", "className": "text-left" },
            { "data": "join_date", "title": "${get_res('join_date','Ngày vào làm')}", "className": "text-center", "format": "date:" + scope.$root.systemConfig.date_format },
            { "data": "email", "title": "${get_res('email','Email')}", "className": "text-left" }
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
    scope._tableData = _tableData;
    scope.mode = 0;
    scope.searchText = "";

    /* Tree */
    scope.$$tree = [{
        treeCurrentNode: {},
        treeSelectedNodes: [],
        treeSelectedRootNodes: [],
        treeCheckAll: false,
        treeSearchText: '',
        treeDisable: false,
        treeMultiSelect: false,
        treeMode: 3,
        treeDataSource: null
    },
    {
        treeCurrentNode: {},
        treeSelectedNodes: [],
        treeSelectedRootNodes: [],
        treeCheckAll: false,
        treeSearchText: '',
        treeDisable: false,
        treeMultiSelect: false,
        treeMode: 3,
        treeDataSource: null
    }];

    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = null;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = null;
    scope.$parent.$parent.$parent.onSave = null;
    scope.$parent.$parent.$parent.onRefresh = function(){
        reloadData();
    };

    scope.$$process_id = scope.$parent.$parent.$parent.$parent.$$table.currentItem.process_id;
    scope.LviewBy = [];
    scope.modeView = 2;

    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        reloadData();
    }

    function reloadData(){
        _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.searchText, scope.$$table.$$tableConfig.fnReloadData);
    }

    function onAdd() {
        if(!scope.$$$perf_cbb_employees){
            (function _getDataInitCombobox() {
                scope.$root.$getInitComboboxData(scope,
                    [{
                        "key": "${encryptor.get_key('perf_cbb_employees')}",
                        "code": null,
                        "alias": "$$$perf_cbb_employees"
                    }
                    ]
                );
            })();
        }
        services.api("${get_api_key('app_main.api.TM_SetupProcessApplyEmp/get_list_employee_in_current_process_and_process_360')}")
        .data({
            process_id : scope.$$process_id
        })
        .done()
        .then(function (response) {
            debugger
            var frm = lv.FormSearch(scope, "$$$perf_cbb_employees");
            var ignoreCode = response;
            var employeeList = {
                list: []
            };
            frm.EmployeeFilter(employeeList, "list", "${get_res('employee_list','Danh sách nhân viên')}", true, ignoreCode);
            frm.openDialog;
            frm.accept(function () {
                debugger
                var parameter = _.map(JSON.parse(JSON.stringify(employeeList.list)), function(val){
                    return {
                        process_id : scope.$$process_id,
                        employee_code : val
                    }
                })
                services.api("${get_api_key('app_main.api.TM_SetupProcessApplyEmp/insert')}")
                .data(parameter)
                .done()
                .then(function (res) {
                    if(res.error == null){
                        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        reloadData();
                    }else{
                        $msg.message("${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}", "${get_global_res('Please_Try_Again','Xin thử vui lòng thử lại')}", function () { });
                    }
                    scope.$$$perf_cbb_employees.value = [];
                    scope.$applyAsync();
                })
            });
            frm.cancel(function () {

            });
        })
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_JobWorking/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            reloadData();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        } else if (res.error !== null || res.error !== "") {
                            $msg.message("${get_global_res('cannot_delete','Không thể xóa')}", "${get_global_res('job_working_is_using','CDCV đang được sử dụng')}", function () { });
                        }
                    })
            });
        }
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TMLS_FactorAppraisal'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
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
        var code = scope.modeView == 0 ? scope.$$tree[0].treeCurrentNode.gjw_code : scope.$$tree[1].treeCurrentNode.department_code;
        code = code ? code : "";
        if(scope.modeView == 2 || (scope.modeView != 2 && (code && code != ""))){
            var sort = {};
            $.each(orderBy, function (i, v) {
                sort[v.columns] = (v.type === "asc") ? 1 : -1;
            });
            sort[orderBy[0].columns] =
                services.api("${get_api_key('app_main.api.TM_SetupProcessApplyEmp/get_list_by_mode')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "process_id": scope.$$process_id,
                    "mode": scope.modeView,
                    "code": code
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

        }else{
            callback({
                recordsTotal: 0,
                recordsFiltered: 0,
                data: []
            });
        }
    }

    function _loadTreeDataSource() {
        if(!scope.$$tree[0].treeDataSource || !scope.$$tree[1].treeDataSource)
        services.api("${get_api_key('app_main.api.HCSLS_JobWorkingGroup/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tree[0].treeDataSource = res;
                scope.$applyAsync();
            })
        services.api("${get_api_key('app_main.api.HCSSYS_Departments/get_list')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tree[1].treeDataSource = res;
                scope.$applyAsync();
            })
    }

    (function _getValueList() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": "LPERF_ViewBy_JobW_Dept"
            })
            .done()
            .then(function (res) {
                scope.LviewBy = res.values;
                scope.viewBy = 1;
                scope.$applyAsync();
            })
    })();

    scope.$watch("$$tree", function (val) {
        reloadData();
    }, true);

    scope.$watch('viewBy', function(val, old){
        switch(val){
            case 1: scope.modeView = 2;break;
            case 2: scope.modeView = 0;
                _loadTreeDataSource();
            break;
            case 3: scope.modeView = 1;
                _loadTreeDataSource();
            break;
        }
        if(val != old)
            reloadData();
        scope.$applyAsync();
    });
});