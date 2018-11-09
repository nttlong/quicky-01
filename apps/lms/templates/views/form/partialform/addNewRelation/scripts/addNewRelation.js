(function (scope){
    debugger
    scope.mode = scope.$parent.___mode;//mode relation
    scope.title = scope.$parent.headerTitle;
    scope.cbbLMSLRelation = scope.$parent.cbbLMSLRelation;
    var __entity_relation = JSON.parse(JSON.stringify(scope.$parent.$$table.currentItem ? scope.$parent.$$table.currentItem : {}));
    scope.entity_relation = scope.mode == 2 ? __entity_relation : {};
    (function __init__(){

    })();
    function _getDataInitCombobox(){
    debugger
        scope.$root.$getInitComboboxData(scope,
				{
                    "key": "${encryptor.get_key('cbb_lmsls_materialcouse')}",
                    "code": (scope.entity_relation && scope.entity_relation.hasOwnProperty('course') && scope.entity_relation.course) ? scope.entity_relation.course: null,
                    "alias": "$$$course_id"
                }
			);
    }
    _getDataInitCombobox();

    scope.onResizeDialog = onResizeDialog;

    function onResizeDialog(){
        $dialog.fullScreen();
    }

    scope.saveNNext = saveNNext;
    scope.saveNClose = saveNClose;

    function saveNNext(){

    }

    function saveNClose(){

    }
})