(function (scope) {
   /* scope.$partialpage = "partialpage/examination_management_template_exam_list";

    scope.createTemplateCategory = function () {
        scope.$root.createTemplateCategory();
    }*/
    scope.$root.extendToolbar = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.$root.currentItem = [];
    scope.isDisplayGird = false;
    scope.isList = true;
    scope.isGrid = false;
    scope.objSearch = {};
    scope.create = function () {
        scope.$root.create();
    }
    scope.edit = function () {
        scope.$root.edit();
    }
    scope.delete = function () {    
        scope.$root.delete();
    }
    scope.deleteOne = function () {
        scope.$root.deleteOne();
    }
    scope.onSearchText = function () {

        scope.searchText = scope.objSearch.$$$modelSearch

    }

    scope.viewExamSummary = function () {
        scope.$root.viewExamSummary();
    }


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
    /*                                                         */
    /* ==================== Property Scope - END ==============*/
    /*                                                         */

    /*                                                         */
    /* ==================== Initialize - START=================*/
    /*                                                         */
    activate();
    init();
    /*                                                         */
    /* ==================== Initialize - END ==================*/
    /*                                                         */

    /*                                                                                          */
    /* ===============================  Implementation - START  ================================*/
    /*                                                                                          */

    /* Object handle data */
    function handleData() {

        this.collection = {};

        this.mapName = [];



        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
    }

    /*                                                                                          */
    /* ===============================  Implementation - END  ==================================*/
    /*                                                                                          */

    scope.$watch("selectedFunction", function (function_id) {
        if (function_id) {
            var $his = scope.$root.$history.data();
            if($his && $his.hasOwnProperty('page') && _.findWhere(scope.$root.$function_list, {'function_id': $his.page}))
                window.location.href = "#page=" + scope.$root.$extension.TripleDES.encrypt($his.page) + "&f=" + scope.$root.$extension.TripleDES.encrypt(function_id);
            else
                window.location.href = "#page=" + scope.$root.$extension.TripleDES.encrypt(scope.$root.$extension.TripleDES.decrypt($his.page)) + "&f=" + scope.$root.$extension.TripleDES.encrypt(function_id);
        }
    });

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        if (scope.mapName.length > 0) {
            if (data.f) {
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
                    scope.selectedFunction = func[0].function_id;
                } else {
                    window.location.href = "#";
                }
            } else {
                scope.$partialpage = scope.mapName[0].url;
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });

});