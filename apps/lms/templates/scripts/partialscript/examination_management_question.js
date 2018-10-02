(function (scope) {
    scope.$root.extendToolbar = true;
    scope.$partialpage = "partialpage/examination_management_question_bank";

    scope.createQuestionCategory = function () {
        scope.$root.createQuestionCategory();
    }
    scope.editQuestionCategory = function () {
        scope.$root.editQuestionCategory();
    }
    scope.delQuestionCategory = function () {
        scope.$root.delQuestionCategory();
    }
});