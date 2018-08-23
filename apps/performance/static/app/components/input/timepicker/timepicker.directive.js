(function () {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('timePicker', timePicker);

    timePicker.$inject = ['$window'];

    function timePicker($window) {
        // Usage:
        //     <time-picker></time-picker>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            template: template(),
            scope: {
                ngModel: "=",
                format: "@"
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
            var _timePicker = element.find('.zb-hour-picker');
            scope.openPicker = function () {
                _timePicker.datetimepicker('show');
            }
            if (callback)
                callback(scope, _timePicker, changeValue)
        }

        function changeValue(scope, val) {
            scope.ngModel = ("0" + val.date._d.getHours()).slice(-2) + ":";
            scope.ngModel += ("0" + val.date._d.getMinutes()).slice(-2) + ":";
            scope.ngModel += ("0" + val.date._d.getSeconds()).slice(-2);
            scope.$applyAsync();
        }

        function compile(scope, timePicker, callback) {
            var hour = null;
            timePicker.datetimepicker({
                format: scope.format
            })
            if (scope.ngModel) {
                hour = scope.ngModel.split(":");
                hour = new Date(2000, 0, 1, hour[0], hour[1], hour[2]);
                timePicker.datetimepicker().data("DateTimePicker").date(hour);
            }
            timePicker.datetimepicker().on('dp.change', function (val) {
                callback(scope, val);
            });
        }

        function template() {
            return `
                <span class="input-group zb-form-date-picker">
                    <input type="text" class="zb-hour-picker">
                    <span class="input-group-btn">
                        <button ng-click="openPicker()" type="button" class="btn btn-default">
                            <i class="bowtie-icon bowtie-stopwatch"></i>
                        </button>
                    </span>
                </span>
                `;
        }
    }

})();