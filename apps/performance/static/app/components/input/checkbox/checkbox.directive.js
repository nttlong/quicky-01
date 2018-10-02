(function () {
    'use strict';

    angular.module('ZebraApp.components.inputs')
        .directive('inputCheckbox', ["$parse", inputCheckbox]);

    /** @ngInject */
    function inputCheckbox($parse) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                model: "=ngModel",
                caption: "@",
                fnChange: "&ngChange",
                ngDisabled: "="
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: "app/components/input/checkbox/checkbox.html",
            link: function ($scope, elem, attr) {
                var input = $(elem.find("input")[0]);
                var div = $(elem);

                if ($scope.ngDisabled) {
                    input.prop("ngDisabled", true);
                    div.addClass("ngDisabled");
                } else {
                    input.prop("ngDisabled", false);
                    div.removeClass("ngDisabled");
                }
                $(elem).find("input[type=checkbox]").change(function () {
                    // if($(this).is(":checked")) {
                    //     var returnVal = confirm("Are you sure?");
                    //     $(this).attr("checked", returnVal);
                    // }
                    // $('#textbox1').val($(this).is(':checked')); 
                    if ($scope.fnChange) {
                        $scope.fnChange();
                    }
                });
            }
        };
    }
})();