(function (scope) {
    scope.$partialpage = null;
    scope.$display = {};
    scope.tableFields = [
        { "data": "exam_id", "title": "${get_res('ID','ID')}" },
        { "data": "exam_name1", "title": "${get_res('exam_name','Exam Name')}" },
        { "data": "exam_type", "title": "${get_res('exam_type','Exam Type')}" },
        { "data": "start_date", "title": "${get_res('start_date','Start Date')}" },
        { "data": "end_date", "title": "${get_res('end_date','End Date')}" },
        { "data": "result_less_name", "title": "${get_res('retake_condition','Retake Condition')}" },
        { "data": "retake_condition", "title": "${get_res('retake_times','Retake Times')}" },
        { "data": "exam_id", "title": "${get_res('no_of_candidates','No.of Candidates')}" },
    ];
    scope.tableSource = _loadDataServerSide;
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
        //if (scope.treeCurrentNode.hasOwnProperty('folder_id')) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_ExExamination/get_exam_retake_list')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    for (var i = 0; i < res.items.length; i++) {
                        if (res.items[i].course_related) {
                            res.items[i].exam_type = "${get_res('course_related','Course-Related')}";
                        } else {
                            res.items[i].exam_type = "${get_res('non_course_related','Non Course-Related')}";
                        }
                        if (res.items[i].result_less) {
                            res.items[i].result_less_name = "> " + res.items[i].result_less;
                        } else {
                            res.items[i].result_less_name = "${get_res('result_less_none','None')}";
                        }
                    }

                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.$apply();
                })
        //}
    }

    /*
     * * Hàm select row của table
     */
    scope.onSelectTableRow = function ($row) {
        scope.$partialpage = "examination_management_retake_detail";
        //
        scope.$display.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });
        //
        scope.$display.selectedFunction = (scope.$display.mapName.length > 0) ? scope.$display.mapName[0].function_id : null;
        //
        scope.$applyAsync();
    };
});