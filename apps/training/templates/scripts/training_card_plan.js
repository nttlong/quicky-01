(function (scope) {
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "course_code", "title": "${get_res('course_code','Mã khóa')}" },
        { "data": "course_name", "title": "${get_res('course_name','Tên khóa đào tạo')}" },
        { "data": "from_day", "title": "${get_res('from_day','Từ ngày')}","format": "date:" + scope.$root.systemConfig.date_format},
        { "data": "to_day", "title": "${get_res('to_day','Đến ngày')}","format": "date:" + scope.$root.systemConfig.date_format },
        { "data": "year", "title": "${get_res('year','Năm')}" },
        { "data": "quarter", "title": "${get_res('quarter','Quý')}" },
        { "data": "wave", "title": "${get_res('wave','Đợt')}" },
        { "data": "check", "title": "${get_res('check','Đã duyệt')}","format": "checkbox" },
        { "data": "scheduler", "title": "${get_res('scheduler','Lập lịch')}","format": "checkbox" },
        { "data": "number", "title": "${get_res('number','Số lượng')}" },
        { "data": "method", "title": "${get_res('method','Phương thức')}" },
        { "data": "address", "title": "${get_res('address','Địa điểm')}" },
        { "data": "room", "title": "${get_res('room','Phòng học')}" },
        { "data": "teacher", "title": "${get_res('teacher','Giáo viên')}" },
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
            services.api("${get_api_key('app_main.api.HCSLS_TrainPlan/get_list_with_searchtext')}")
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
        openDialog("${get_res('Create_train_plan','Chi tiết kế hoạch đào tạo')}", 'form/addTrainPlan', function () {
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
            openDialog("${get_res('Edit_train_plan','Chi tiết kế hoạch đào tạo')}", 'form/addTrainPlan', function () { });
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
                services.api("${get_api_key('app_main.api.HCSLS_TrainPlan/delete')}")
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