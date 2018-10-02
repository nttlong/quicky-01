(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('yearPicker', yearPicker);

    yearPicker.$inject = ['$window'];
    
    function yearPicker ($window) {
        // Usage:
        //     <year-picker></year-picker>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'EA',
            template: template();
            scope: {
                ngModel:"="
            }
        };
        return directive;

        function link(scope, element, attrs) {
            compile(scope, element);
        }

        function initialize() {

        }

        function compile(scope, element) {
            element.find('.zb-year-picker').datepicker({
                format: "yyyy",
                startView: 2,
                minViewMode: 2,
                multidate: true,
                clearBtn: true
            }).on('changeDate', function (val) {

            }).datepicker('setDates', [new Date(2011, 2, 5)]);
        }

        function template() {
            return `
                <span class="input-group zb-form-date-picker">
                     <input type="text" class="zb-year-picker"><span class="input-group-addon"><i class="bowtie-icon bowtie-calendar-month"></i></span>
                </span>
                `;
        }
    }

})();