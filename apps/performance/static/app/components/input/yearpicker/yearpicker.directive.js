(function () {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('yearPicker', yearPicker);

    yearPicker.$inject = ['$window'];

    function yearPicker($window) {
        // Usage:
        //     <year-picker></year-picker>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            template: template(),
            scope: {
                ngModel: "=",
                multi: "=",
                language: "@",
                ngDisabled: "="
            }
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs.hasOwnProperty('required')) {
                $(element).wrap("<span zb-required></span>")
            }
            initialize(scope, element, compile)
        }

        function initialize(scope, element, callback) {
            if (scope.multi && !Array.isArray(scope.ngModel)) {
                console.error('year picker multi select require ngModel is array')
                if (!scope.ngModel)
                    scope.ngModel = [];
            }
            var _yearPicker = element.find('.zb-year-picker');
            scope.openPicker = function () {
                _yearPicker.datepicker('show');
            }
            if (callback)
                callback(scope, _yearPicker, changeValue)
        }

        function changeValue(scope, val) {
            if (scope.multi) {
                scope.ngModel = _.map(val.dates, function (val) {
                    return val.getFullYear();
                })
            } else {
                scope.ngModel = val.date.getFullYear();
            }
            scope.$applyAsync();
        }

        function compile(scope, yearPicker, callback) {
            var dates = null;
            yearPicker.datepicker({
                format: "yyyy",
                startView: 2,
                minViewMode: 2,
                multidate: scope.multi,
                clearBtn: true,
                language: scope.language ? scope.language : "en"
            })
            if (scope.multi) {
                if (scope.ngModel.length > 0) {
                    dates = _.map(scope.ngModel, function (val) {
                        return new Date(val, 0, 1);
                    });
                    yearPicker.datepicker('setDates', dates);
                }
            } else {
                if (scope.ngModel) {
                    dates = new Date(scope.ngModel, 0, 1);
                    yearPicker.datepicker('setDate', dates);
                }
            }
            yearPicker.datepicker().on('changeDate', function (val) {
                callback(scope, val);
            });
            scope.$watch('ngModel', function (oldVal, newVal) {
                if (newVal && (oldVal != newVal)) {
                    var data = _.map(scope.ngModel, function (val) {
                        return new Date(val, 0, 1);
                    });
                    yearPicker.datepicker('setDates', data);
                }
            }, true);
        }

        function template() {
            return ''
                + '<span class="input-group zb-form-date-picker">'
                + '    <input type="text" class="zb-year-picker" ng-disabled="ngDisabled">'
                + '    <span class="input-group-btn">'
                + '        <button ng-click="openPicker()" type="button" class="btn btn-default" ng-disabled="ngDisabled">'
                + '            <i class="bowtie-icon bowtie-calendar-month"></i>'
                + '        </button>'
                + '    </span>'
                + '</span>'
                ;
        }
    }

})();