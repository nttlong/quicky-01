(function () {
    'use strict';

    angular.module('ZebraApp.components.combobox')
        .directive('bsDatetimePicker', ["$compile", bsDatetimePicker]);

    /** @ngInject */
    function bsDatetimePicker($compile) {
        return {
            restrict: 'E',
            replace: true,
            //transclude: true,
            scope: {
                defaultValue: "@",
                ngModel: "=",
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            template: `
                <div class="zb-form-combobox input-group date">
                    <input type="text"  class="form-control zb-form-input">
                    <div class="input-group-btn input-group-addon"
                        style="padding: 0; border: unset; border-radius: unset;">
                        <button type="button" class="btn btn-default" style="border-bottom: 1px solid #cbcbcb;">
                            <i class="glyphicon glyphicon-calendar"></i>
                        </button>
                    </div>
                </div>
            `,
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr) {
                debugger;
                var lang = $scope.$root.language;
                var date_format = $scope.$root.systemConfig.date_format;
                var map_date_format = $scope.$root.systemConfig.map_date_format ? $scope.$root.systemConfig.map_date_format : [
                    { 'dd': 'DD' },
                    { 'yy': 'YY' },
                    { 'yyyy': 'YYYY' }
                ];
                var arrDate = date_format.split('/');
                var strFormat = '';
                arrDate.forEach(function(v) {
                    var item = _.find(map_date_format, function (o) { return o[v]; })
                    if(item && item[v]){
                        strFormat+= item[v] + '/'
                    } else {
                        strFormat+= v + '/'
                    }
                })
                strFormat = strFormat.slice(0, -1) + ' | hh:mm';
                if(lang == 'vn' || lang == 'vi'){
                    moment.updateLocale('vi', {
                        months : [
                            "Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5", "Tháng 6", "Tháng 7",
                            "Tháng 8", "Tháng 9", "Tháng 10", "Tháng 11", "Tháng 12"
                        ]
                    });
                }
                $(elem).datetimepicker({
                    locale: lang,
                    format: strFormat,
                    defaultDate: $scope.defaultValue ? $scope.defaultValue : $scope.ngModel
                }).on('dp.change', function (e) {
                    $scope.ngModel = e.date.format(e.date._f);
                });
            }
        };
    }
})();