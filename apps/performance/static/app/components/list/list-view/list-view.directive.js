(function () {
    'use strict';

    angular
        .module('ZebraApp.components.lists')
        .directive('listView', listView)
        .directive('listViewTemplate', listViewTemplate);

    listView.$inject = ['$window', '$parse', '$compile'];
    listViewTemplate.$inject = ['$window', '$parse', '$compile'];

    function listViewTemplate($window, $parse, $compile){
        debugger
        // Usage:
        //     <tag-name list-view-template></tag-name>
        // Creates:
        // 
        var directive = {
            restrict: "ECA",
            link: link
        }
        return directive;

        function link(scope, element, attrs){
            $(element[0]).parent().attr("data-template",element[0].outerHTML);
            element.remove();
        }
    }

    function listView($window, $parse, $compile) {
        // Usage:
        //     <list-view></list-view>
        // Creates:
        // 
        var directive = {
            link: link,
            transclude: true,
            restrict: 'EA',
            template: template(),
            scope: {
                captionField: "@",
                valueField: "@",
                source: "=",
                ngModel: "=",
                ngChange: "=",
                multi: "=",
                textSearch: "="
            }
        };
        return directive;

        function link(scope, element, attrs) {
            scope.isCustomTemplate = element.find("[ng-transclude]").attr("data-template") ? true : false;
            if(element.find("[ng-transclude]").attr("data-template")){
                var html = element.find("[ng-transclude]").attr("data-template");
                var compileTemplate = $("<div>"+html+"</div>");
                compileTemplate.children().removeAttr('list-view-template'); 
                compileTemplate.children().attr('ng-repeat', 'item in listView | filter : testSearch'); //repeat template each data row
                compileTemplate.children().attr('ng-click', 'deSelected($event, item, $index)');

                scope.listView = [{
                    A : "1",
                    B : "2",
                    C : "3",
                    D : "4"
                },
                {
                    A : "5",
                    B : "6",
                    C : "7",
                    D : "8"
                },
                {
                    A : "5",
                    B : "6",
                    C : "7",
                    D : "8"
                },
                {
                    A : "5",
                    B : "6",
                    C : "7",
                    D : "8"
                },
                {
                    A : "5",
                    B : "6",
                    C : "7",
                    D : "8"
                }];

                scope.objecyKeys = {};
                if(scope.valueField){
                    _.each(scope.valueField.slit(','), function(val){
                        if(val){
                            val.trim();
                            scope.objecyKeys[val.trim()] = null;
                        }
                    });
                }

                scope.deSelected = function(event, item, index){
                    var param = _.mapObject(scope.objecyKeys, function(val, key) { 
                        return val = item[key] ? item[key] : null 
                    });
                    if(scope.multi && scope.multi === true){
                        if($(event.currentTarget).hasClass('active')){
                            $(event.currentTarget).removeClass('active');
                            _.reject(scope.ngModel, param);
                        }
                        else{
                            $(event.currentTarget).addClass('active');
                        }
                    }else{
                        element.find('[ng-transclude]').children().removeClass('active');
                        $(event.currentTarget).addClass('active');
                        scope.ngModel = item;
                    }
                }

                compileTemplate.children().appendTo(element.find("[ng-transclude]")[0]);

                $compile(element.find("[ng-transclude]").children())(scope);
                scope.$apply();
            }else{
                scope.selectItem = function (event, item) {
                    if (scope.multi) {
                        if (_.findWhere(scope.ngModel, JSON.parse(angular.toJson(item)))) {
                            scope.ngModel = _.reject(scope.ngModel, JSON.parse(angular.toJson(item)));
                        } else {
                            scope.ngModel = _.uniq(_.union(scope.ngModel, [JSON.parse(angular.toJson(item))]), false, _.property(scope.valueField));
                        }
                    } else {
                        scope.ngModel = JSON.parse(angular.toJson(item))
                    }
                    if (scope.ngChange)
                        scope.ngChange()(scope.ngModel);
                }

                scope._contains = function (source, value) {
                    return _.findWhere(source, JSON.parse(angular.toJson(value))) ? true : false;
                }

                scope._equal = function (TSource, Tdes) {
                    return _.isEqual(JSON.parse(angular.toJson(TSource)), JSON.parse(angular.toJson(Tdes)))
                }
            }
        }
    }

    function template() {
        return `
                <div class ="list-group zb-list-view" ng-if="!multi">
                    <a ng-if="!isCustomTemplate" ng-repeat="elm in source | filter : textSearch track by $index" ng-class="{active:_equal(ngModel, elm)}" class ="list-group-item" ng-click="selectItem($event, elm)">{{elm[captionField]}}</a>
                    <div ng-transclude></div>
                </div>
                <div class ="list-group zb-list-view" ng-if="multi">
                    <a ng-if="!isCustomTemplate" ng-repeat="elm in source| filter : textSearch track by $index" ng-class="{active:_contains(ngModel, elm)}" class ="list-group-item" ng-click="selectItem($event, elm)">{{elm[captionField]}}</a>
                    <div ng-transclude></div>
                </div>
            `;
    }

})();