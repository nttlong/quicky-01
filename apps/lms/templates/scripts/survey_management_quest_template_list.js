(function (scope) {
    scope.filterFunctionModel = ''
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
        debugger
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
});