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
});