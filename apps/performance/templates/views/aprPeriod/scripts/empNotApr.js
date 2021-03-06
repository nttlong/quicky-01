﻿﻿(function (scope) {

    scope.__tableSource = [];
    scope.tableFields = [
        { "data": "employee_code", "title": "${get_res('employee_code_header','Mã nhân viên')}" },
        { "data": "employee_name", "title": "${get_res('employee_nametable_header','Họ tên')}" },
        { "data": "department_code", "title": "${get_res('department_code_table_header','Bộ phận')}" },
        { "data": "job_w_code", "title": "${get_res('job_w_code_table_header','Chức danh')}" },
        { "data": "reason", "title": "${get_res('reason_table_header','Lý do')}" },
        { "data": "note", "title": "${get_res('note_header','Ghi chú')}" }
    ];
    scope.$$tableConfig = {};
    scope._tableData = _tableData;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        openDialog("${get_res('An_Employee_Not_Aproval_Detail','Chi tiết Nhân viên không đánh giá')}", 'aprPeriod/form/editAnEmpNotApr', function () { });
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    //Refesh table
    scope.refreshDataRow = function () { /*Do nothing*/ };

    scope.$parent.$parent.$parent.onGen = onGenDataGeneration;
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;
    scope.onExport = onExport;
    scope.onImport = onImport;

    function onSearch(val){
        scope.tableSearchText = val;
        scope.$apply();
    }

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
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.TMPER_AprPeriod/get_empNotApr_by_apr_period')}")
                .data({
                    "apr_period": scope.$parent.mode == 1 ? scope.$parent.apr_period_now : scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period),
                    "apr_year": scope.$parent.mode == 1 ? scope.$parent.apr_year_now : scope.$parent.entity.apr_year,
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    scope.apr_period_emp_out = JSON.parse(JSON.stringify(res.items));
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

    function onGenDataGeneration() {
        scope.mode = 4;// set mode tạo mới
        scope.$apr_period = scope.$parent.mode == 1 ? scope.$parent.apr_period_now : scope.$parent.entity.apr_period;
        scope.$apr_year = scope.$parent.mode == 1 ? scope.$parent.apr_year_now : scope.$parent.apr_year_now;
        openDialog("${get_res('generate_data','Phát sinh Danh sách nhân viên không đánh giá')}", 'aprPeriod/form/genEmpNotApr', function () { });
        
    };

    function onAdd() {

        scope.entity = {};
        scope.entity.list_nv = [];
        var frm = lv.FormSearch(scope, "$$$perf_cbb_employees");
        frm.EmployeeFilter(scope.entity, "list_nv", "${get_res('job_w_change','CDCV có thể thuyên chuyển')}", true);
        frm.openDialog;
        frm.accept(function () {
            console.log("@@@@", scope.entity.list_nv);
            // call server to get multi nv by emp_code and insert data to TMPER_AprPeriodEmpOut
                // => generate department_code and job_w_code, apr_year, apr_period
            services.api("${get_api_key('app_main.api.TMPER_AprPeriodEmpOut/get_insert_multi_empNotApr')}")
                .data({
                    apr_period : scope.$parent.$parent.$parent.Re_Map_Period(scope.$parent.$parent.$parent.entity.apr_period),
                    apr_year: scope.$parent.$parent.$parent.entity.apr_year,
                    list_emp: scope.entity.list_nv 
                })
                .done()
                .then(function (res) {
                    if (res.error == null) {
                        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                        $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                        scope.$applyAsync();

                        scope.currentItem = null;
                        scope.selectedItems = [];
                    }
                })
        });
        frm.cancel(function () {
        });
    };

    function onDelete() {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMPER_AprPeriodEmpOut/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();

                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    };

    function onEdit() {
        if (scope.currentItem || scope.selectedItems.length > 0) {
            scope.mode = 2;
            (scope.selectedItems.length == 1 || scope.selectedItems.length == 0) ?
                openDialog("${get_res('An_Employee_Not_Aproval_Detail','Chi tiết Nhân viên không đánh giá')}", 'aprPeriod/form/editAnEmpNotApr', function () { }) :
                openDialog("${get_res('Multi_Employee_Not_Aproval_Detail','Chi tiết Nhân viên không đánh giá')}", 'aprPeriod/form/editMultiEmpNotApr', function () { });
        }
        else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };

    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'HCSLS_EmployeeType'
            }).done();
    }

    function onAttach() {

    };
    function onRefresh() {
        _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText,
            scope.$$tableConfig.fnReloadData);
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
});