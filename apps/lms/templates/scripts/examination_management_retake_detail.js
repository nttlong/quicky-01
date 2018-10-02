(function (scope) {
    scope.$display = {};
    (function _init_() {
        scope.$display.mapName = scope.$parent.$display.mapName;
        scope.currentFunction = scope.$display.mapName[0];
        scope.$display.selectedFunction = scope.$parent.$display.selectedFunction;
        scope.$applyAsync();
    })();
});