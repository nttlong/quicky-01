(function (scope) {
    scope._page = [
        "updateTarget/list",
        "updateTarget/detail"
    ]
    scope.$partialPage = scope._page[0];
    scope.onEdit = function(){
        scope.$partialPage = scope.$partialPage === scope._page[0] ? scope._page[1] : scope._page[0];
    };
    scope.backPage = function(){
        scope.$partialPage = scope._page[0];
        scope.$applyAsync();
    }
});