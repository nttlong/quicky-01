(function () {
    'use strict';

    angular
        .module('ZebraApp.components.lists')
        .directive('listView', listView);

    listView.$inject = ['$window', '$parse', '$compile'];

    function listView($window, $parse, $compile) {
        // Usage:
        //     <list-view></list-view>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            template: template(),
            scope: {
                captionField: "@",
                valueField: "@",
                source: "=data",
                ngModel: "=",
                ngChange: "&",
                multi: "="
            }
        };
        return directive;

        function link(scope, element, attrs) {
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
            }

            scope._contains = function (source, value) {
                return _.findWhere(source, JSON.parse(angular.toJson(value))) ? true : false;
            }

            scope._equal = function (TSource, Tdes) {
                return _.isEqual(JSON.parse(angular.toJson(TSource)), JSON.parse(angular.toJson(Tdes)))
            }
        }
    }

    function template() {
        return `
              <div class ="list-group zb-list-view" ng-if="!multi">
                <a ng-repeat="elm in source track by $index" ng-class="{active:_equal(ngModel, elm)}" class ="list-group-item" ng-click="selectItem($event, elm)">{{captionField}}</a>
              </div>
              <div class ="list-group zb-list-view" ng-if="multi">
                <a ng-repeat="elm in source track by $index" ng-class="{active:_contains(ngModel, elm)}" class ="list-group-item" ng-click="selectItem($event, elm)">{{captionField}}</a>
              </div>
            `;
    }

})();