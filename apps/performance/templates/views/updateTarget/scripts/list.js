(function(scope){
    scope.$parent.onEdit = function(){
        scope.$parent.$partialPage = scope.$parent.$partialPage === scope.$parent._page[0] ? scope.$parent._page[1] : scope.$parent._page[0];
    };
});