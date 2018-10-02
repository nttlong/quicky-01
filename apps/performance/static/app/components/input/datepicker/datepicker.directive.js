(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('datePicker', ["$parse", "$filter", "$sce", inputSelect]);

    /** @ngInject */
    function inputSelect($parse, $filter, $sce) {
        return {
            restrict: 'E',
            replace: true,
            scope: {
                dt: "=ngModel",
                format: "@",
                ngDisabled: "="
            },
            //transclude: true,
            //template: '<input type="text" class="form-control zb-form-input"/>',
            templateUrl: "app/components/input/datepicker/datepicker.html",
            link: function ($scope, elem, attr) {
                if (attr["required"]) {
                    $(elem).attr("zb-required", '');
                }

                $scope.opened = false;
                $scope.format = ($scope.format) ? $scope.format : 'dd-MM-yyyy';
                $scope.options = {
                    showWeeks: false
                };

                $loadLayout($scope, elem, attr);

                $scope.$watch("dt", function (val, old) {
                    $scope.opened = false;
                    // if (val) {
                    //     $scope.dt = new Date($scope.dt);
                    // } else {    
                    //     $scope.dt = new Date();
                    // }
                    if (!angular.isDate(val)) {
                        var _default = new Date();
                        var _dateValue = new Date(val);
                        $scope.dt = ($scope.dt) ? 
                        new Date(Date.UTC(_dateValue.getFullYear(), _dateValue.getMonth(), _dateValue.getDate(), _dateValue.getHours(), _dateValue.getMinutes(), _dateValue.getSeconds())) 
                        : null;
                    }

                    $scope.$applyAsync();
                });
            }
        };
    }

    function $loadLayout($scope, elem, attr) {
        var btnCalendar = $(elem.find("button.btn-default")[0]);
        var inputDate = $(elem.find("input")[0]);

        btnCalendar.unbind("click");
        btnCalendar.bind("click", function () {
            $scope.opened = true;
            $scope.$apply();
        });
    }

})();