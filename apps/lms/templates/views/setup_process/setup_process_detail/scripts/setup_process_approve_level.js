(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "approve_level", "title": "${get_res('approve_level','Số cấp duyệt')}" },
            { "data": "approver_value", "title": "${get_res('approver_value','Người duyệt')}" },
            { "data": "email_approve_code", "title": "${get_res('email_approve_code','Email duyệt')}" },
            { "data": "email_approve_to_name", "title": "${get_res('email_approve_to','Gửi tới')}" },
            { "data": "email_reject_code", "title": "${get_res('email_reject_code','Email không duyệt')}" },
            { "data": "email_reject_to", "title": "${get_res('email_reject_to','Gửi tới')}" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope.__mode = scope.$parent.$parent.$parent.$parent.mode;
    scope.$$process_id = scope.__mode == 2 ? scope.$parent.$parent.$parent.$parent.$$table.currentItem.process_id : null;
    scope.$$curr_max_approve_level = scope.__mode == 2 ? JSON.parse(JSON.stringify(scope.$parent.$parent.$parent.$parent.$$table.currentItem.max_approve_level)) : 0;
    //debugger
    //scope.$parent.$parent.$parent.$parent.onAdd = onAdd;

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
            services.api("${get_api_key('app_main.api.LMS_SetupProcessApproveLevel/get_list_approve_level_by_process_id')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "process_id": scope.$$process_id
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
    scope.onAdd = function () {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_performance','Chi tiết Tiêu chuẩn năng suất')}",
            'jobworkingpanel/jobworkingdetail/form/addPerformanceStandard', function () { });
    };
    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_Function_And_Mission','Chi tiết Tiêu chuẩn năng suất')}", 'jobworkingpanel/jobworkingdetail/form/addPerformanceStandard', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
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
});