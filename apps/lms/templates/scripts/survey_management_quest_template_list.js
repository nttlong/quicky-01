(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "survey_id", "title": "${get_res('id','ID')}", "className": "text-left" },
            { "data": "temp_survey_1", "title": "${get_res('temp_survey_name','Tên mẫu khảo sát')}", "className": "text-left" },
            { "data": "survey_type_name", "title": "${get_res('survey_type_name','Loại khảo sát')}", "className": "text-left" },
            { "data": "total_question", "title": "${get_res('total_question','Tổng số câu hỏi')}", "className": "text-center", "expr": function(row, columns, func){
                func(function(){
                    return row.question_list ? row.question_list.length : 0;
                })
                return true;
            } },
            { "data": "created_on", "title": "${get_global_res('created_on','Ngày tạo')}", "format": "date:" + scope.$root.systemConfig.date_format, "className": "text-center" },
            { "data": "active", "width":"50px", "title": "${get_res('disabled','Ngưng sử dụng')}", "format": "checkbox", "className": "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) {
            scope.onEdit();
        },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope.$$typeSurvey = null;

    scope.filterFunctionModel = '';
    scope.currentFunction = '';
    scope.mapName = [];
    scope.cbbSysLock = [];
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.advancedSearch = {
        data_lock: null,
    }
    scope.$applyAsync();

    init();

    scope.onAdd = onAdd;
    scope.onEdit = onEdit;
    scope.onDelete = onDelete;
    scope.onImport = onImport;
    scope.onExport = onExport;
    scope.onRefresh = onRefresh;
    scope.onSearch = onSearch;

    function handleData() {

        this.mapName = [{
                            default_name: "${get_res('all_surveys','All Surveys')}",
                            custom_name: "${get_res('all_surveys','All Surveys')}",
                            url: "partialpage/survey_management_template_all_surveys",
                            icon: "bowtie-icon bowtie-dictionary",
                            sorting: "1",
                            active: true,
                            function_id: "LMS_SUR_TEMP0001"
                        },
                        {
                            default_name: "${get_res('course_evaluation_by_students','Course Evaluation By Student')}",
                            custom_name: "${get_res('course_evaluation_by_students','Course Evaluation By Student')}",
                            url: "partialpage/survey_management_template_course_evaluation_by_students",
                            icon: "bowtie-icon bowtie-dictionary",
                            sorting: "2",
                            active: true,
                            function_id: "LMS_SUR_TEMP0002"
                        },
                        {
                            default_name: "${get_res('course_evaluation_by_teachers','Course Evaluation By Teachers')}",
                            custom_name: "${get_res('course_evaluation_by_teachers','Course Evaluation By Teachers')}",
                            url: "partialpage/survey_management_template_course_evaluation_by_teachers",
                            icon: "bowtie-icon bowtie-dictionary",
                            sorting: "3",
                            active: true,
                            function_id: "LMS_SUR_TEMP0003"
                        },
                        {
                            default_name: "${get_res('course_evaluation_by_training_dept','Course Evaluation By Training Dept')}",
                            custom_name: "${get_res('course_evaluation_by_training_dept','Course Evaluation By Training Dept')}",
                            url: "partialpage/survey_management_template_course_evaluation_by_training_dept",
                            icon: "bowtie-icon bowtie-dictionary",
                            sorting: "4",
                            active: true,
                            function_id: "LMS_SUR_TEMP0004"
                        }];

    };

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": "sysLock"
            })
            .done()
            .then(function (res) {
                delete res.language;
                delete res.list_name;
                scope.cbbSysLock = res.values;
                scope.advancedSearch.data_lock = "0";
                scope.$applyAsync();
            })
    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0].function_id;
        scope.$partialpage = scope.mapName[0].url;
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        _comboboxData();
    }

    scope.$watch("currentFunction", function (function_id) {
        scope.$partialpage = _.findWhere(scope.mapName, {"function_id" : function_id}).url;
    });

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

    function openDialog(title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    function onSearch(val) {
        scope.$$table.tableSearchText = val;
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
            scope.$apply();
    }
    function onAdd() {
        scope.mode = 1;
        openDialog("${get_res('add_survey_template','Thêm mẫu khảo sát')}", 'form/addSurveyTemplate', function () { });
    };
    function onEdit() {
        debugger
        if (scope.$$table.currentItem) {
            scope.mode = 2;
            openDialog("${get_res('details_survey_template','Chi tiết mẫu khảo sát')}" + ": " + scope.$$table.currentItem.temp_survey_1, 'form/addSurveyTemplate', function () { });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    };
    function onDelete() {
        if (!scope.$$table.selectedItems || scope.$$table.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMS_SurveyTemplateController/delete')}")
                    .data(scope.$$table.selectedItems)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _tableData(scope.$$table.$$tableConfig.iPage, scope.$$table.$$tableConfig.iPageLength, scope.$$table.$$tableConfig.orderBy, scope.$$table.$$tableConfig.SearchText, scope.$$table.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$$table.currentItem = null;
                            scope.$$table.selectedItems = [];
                        }
                    })
            });
        }
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'TMLS_Competency'
            }).done();
    }
    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    }
    function onRefresh() {
        var tableConfig = scope.$$table.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
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
        services.api("${get_api_key('app_main.api.LMS_SurveyTemplateController/get_list')}")
            .data({
                //parameter at here
                "pageIndex": iPage - 1,
                "pageSize": iPageLength,
                "search": searchText,
                "sort": sort,
                "where": {
                    survey_type: scope.$$typeSurvey
                }
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

    scope.reloadData = function (){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
    }

});