(function (scope){
    scope.entity = scope.$parent.entity;
    scope.__mode = scope.$parent.__mode;

    (function __init__(){
        debugger
        scope.vll_LMSEx_ques_type = scope.$parent.vll_LMSEx_ques_type;
        scope.vll_LMSEx_ques_level = scope.$parent.vll_LMSEx_ques_level
    })()

    function _getDataInitCombobox() {
        scope.$root.$getInitComboboxData(scope, [{
            "key": "${encryptor.get_key('lms_cbb_employees')}",
            "code": scope.entity.ques_evaluated_by ? scope.entity.ques_evaluated_by : null,
            "alias": "cbb_employees"
        },{
            "key": "${encryptor.get_key('lms_cbb_exQuestionCategory')}",
            "code": scope.entity.ques_category ? scope.entity.ques_category : null,
            "alias": "cbb_excategory"
        }]);
    }
    _getDataInitCombobox();
})