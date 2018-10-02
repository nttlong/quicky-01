(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputMultiSelect', inputMultiSelect)
        .controller('SelectpickerMultiPanelCtrl', SelectpickerMultiPanelCtrl);

    inputMultiSelect.$inject = ['$window'];

    function SelectpickerMultiPanelCtrl($scope, $sce) {

    }

    function inputMultiSelect ($window) {
        // Usage:
        //     <input-multi-select></input-multi-select>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'E',
            controller: SelectpickerMultiPanelCtrl,
            template: template(),
            scope: {
                list: "=",
                ngModel: "=",
                placeholder: "@",
                fieldValue: "@value",
                fieldCaption: "@caption",
                ngDisabled: "=",
                ngChange: "="
            }
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs.hasOwnProperty('required')) {
                $(element).wrap("<span zb-required></span>")
            }
            scope.withDeleteItem = {};
            scope.withDeleteSelectItems = {};
            scope.withDeleteSelectItems = scope.$parent.list;
            scope.setCaption = function () {
                if (scope.ngModel && scope.ngModel.length > 0) {
                    scope.withDeleteSelectItems.selected = [];
                    _.each(scope.withDeleteSelectItems, function (val) {
                        if (scope.ngModel.includes(val[scope.fieldValue])) {
                            scope.withDeleteSelectItems.selected.push(val);
                        }
                    });
                }
            }
            scope.setValue = function () {
                scope.ngModel = _.pluck(scope.withDeleteSelectItems.selected, scope.fieldValue);
                if (scope.ngChange)
                    scope.ngChange()(scope.ngModel);
                scope.$applyAsync();
            }
            scope.$watch('list', function (val) {
                if (val && val.length > 0) {
                    scope.withDeleteSelectItems = val;
                    scope.setCaption();
                }
            })
        }

        function template() {
            return ''
            + '<div class="ng-cloak zb-multi-select" ng-controller="SelectpickerMultiPanelCtrl" ng-disabled="ngDisabled">'
            + '    <div class="form-group ">'
            + '            <ui-select multiple ng-change="setValue()" ng-model="withDeleteSelectItems.selected" ng-disabled="ngDisabled" search-enabled="true" append-to-body="false" class="form-control form-control">'
            + '                <ui-select-match placeholder="{{placeholder}}">'
            + '                    {{$item[fieldCaption]}}'
            + '                </ui-select-match>'
            + '                <ui-select-choices repeat="withDeleteItem in withDeleteSelectItems | filter: $select.search">'
            + '                    {{withDeleteItem[fieldCaption]}}'
            + '                </ui-select-choices>'
            + '            </ui-select>'
            + '            <span>'
            + '            </span>'
            + '    </div>'
            + '    <i class="caret pull-right" ng-show="withDeleteSelectItems.selected.length == 0"></i>'
            + '</div>'
            ;
        }
    }

})();