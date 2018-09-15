$("body").attr("ng-controller","app")
var app=angular.module("app",["c-ui"])
app.controller("app",["$compile","$dialog","$filter","$scope",function($compile,$dialog,$filter,scope){
    if(window.appReady){
        window.appReady(scope);
    }
    scope.$applyAsync();
}]);
var x=angular.bootstrap(document,["app","ui"])