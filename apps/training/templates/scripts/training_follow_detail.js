(function (scope) {
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "request_code", "title": "${get_res('request_code','Mã phiếu')}" },
        { "data": "course_name", "title": "${get_res('course_name','Tên khóa đào tạo')}" },
        { "data": "reason_train", "title": "${get_res('reason_train','Lý do đào tạo')}" },
        { "data": "year", "title": "${get_res('year','Năm')}" },
        { "data": "quarter", "title": "${get_res('quarter','Quý')}" },
        { "data": "month", "title": "${get_res('month','Tháng')}" },
        { "data": "cost_estimate", "title": "${get_res('cost_estimate','Chi phí dự kiến')}" },
        { "data": "address", "title": "${get_res('address','Địa điểm')}" },
        { "data": "department_request", "title": "${get_res('department_request','Bộ phận yêu cầu')}" },
        { "data": "proponent", "title": "${get_res('proponent','Người đề nghị')}" },
    ];
    scope.onSelectTableRow = pressEnter;
    scope.tableSource = _loadDataServerSide;
    scope._tableData = _tableData;

    scope.$parent.$parent.$parent.onSearch = onSearch;
    function pressEnter($row) {
        scope.editRoom();
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

    //
    scope.tableSearchText = '';
    scope.SearchText = '';
    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
    debugger
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "desc") ? -1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSLS_TrainRequest/get_list_with_searchtext')}")
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
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    // Insert
    scope.$parent.$parent.$parent.addRoom = function () {
    debugger
        scope.mode = 1; // set mode chỉnh sửa
        openDialog("${get_res('Create_follow','Chi tiết thông tin chung')}", 'form/addTrainFollowDetail', function () {
            setTimeout(function () {
                $(window).trigger('resize');
            }, 200);
        });
    }
    /**
    * Hàm mở form chỉnh sửa
    */
    scope.editRoom = scope.$parent.$parent.$parent.editRoom = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Edit_follow','Chi tiết thông tin chung')}", 'form/addTrainRequest', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    /**
    * Hàm mở form delete
    */
    scope.$parent.$parent.$parent.delRoom = function () {
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.HCSLS_TrainRequest/delete')}")
                    .data(angular.fromJson(angular.toJson(scope.selectedItems)))
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    }
    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$apply();
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

});