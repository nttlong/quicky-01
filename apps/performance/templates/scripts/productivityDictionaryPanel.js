﻿(function (scope) {
    /*                                                         */
    /* ==================== Property Scope - START=============*/
    /*                                                         */
    scope.isChangeFunc = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.cbbSysLock = [];
    scope.selectFunc = function (event, f) {
        scope.selectedFunction = f;
    }
    scope.advancedSearch = {
        data_lock: "0",
    }
    scope.$applyAsync();
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

        this.mapName =_.filter(scope.$root.$function_list,  function(f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    function _comboboxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                //parameter at here
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

    /* Initialize Data */
    function activate() {

    }

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
        _comboboxData();
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