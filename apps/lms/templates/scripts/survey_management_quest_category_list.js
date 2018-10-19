(function (scope) {

    scope.$$table = {
        tableFields: [
            { "data": "category_id", "title": "${get_res('id','ID')}", "className": "text-left" },
            { "data": "category_name", "title": "${get_res('question_category_name','Tên')}", "className": "text-left" },
            { "data": "question_group_display", "title": "${get_res('question_group','Nhóm câu hỏi')}", "className": "text-left" },
            { "data": "num_of_questions", "title": "${get_res('number_of_questions','Số câu hỏi')}", "className": "text-center" },
            { "data": "created_on", "title": "${get_global_res('created_on','Ngày tạo')}", "format": "date:" + scope.$root.systemConfig.date_format, "className": "text-center" },
            { "data": "ordinal", "width":"50px", "title": "${get_global_res('ordinal','Thứ tự')}", "className": "text-center" },
            { "data": "active", "width":"50px", "title": "${get_res('disabled','Ngưng sử dụng')}", "format": "checkbox", "className": "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { scope.onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    scope.onAdd = function(){
        scope.mode = 1;
        openDialog("${get_res('create_new_question_category','Tạo mới nhóm câu hỏi')}", "form/addSurQuestionCategory", function(){});
    }

    scope.onEdit = function(){
        scope.mode = 2;
        openDialog("${get_res('edit_question_category','Chỉnh sửa nhóm câu hỏi')}", "form/addSurQuestionCategory", function(){});
    }

    scope.reloadData = function (){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
    }

    scope.onDelete = function(){
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMS_SurQuestionCategoryController/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.reloadData();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            }).cancel(function () {
                
            }).deny(function () {
                
            });
        }
    }

    scope.onImport = function(){
        
    }

    scope.onExport = function(){
        
    }

    scope.onRefresh = function(){
        scope.reloadData();
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
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
        services.api("${get_api_key('app_main.api.LMS_SurQuestionCategoryController/get_list')}")
            .data({
                //parameter at here
                "pageIndex": iPage - 1,
                "pageSize": iPageLength,
                "search": searchText,
                "sort": sort
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
                    scope.$$table.currentItem = null;
                    scope.$apply();
                }
            })
    }

    init();

    function openDialog(title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    function init() {
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
    }

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
        {
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        }else{
            window.location.href = '#page=' + scope.$root.$extension.TripleDES.encrypt(data['page']);
        }
    });
});