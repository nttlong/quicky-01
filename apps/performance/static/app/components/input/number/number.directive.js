(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputNumber', inputNumber);

    inputNumber.$inject = ['$window', "$parse", "$filter", "$locale", "templateService"];
    
    function inputNumber($window, $parse, $filter, $locale, templateService) {
        // Usage:
        //     <input-number></input-number>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'ECA',
            templateUrl: templateService.getStatic("app/components/input/number/number.html"),
            scope: {
                ngModel: "=",
                ngChange: "&",
                ngDisabled: "="
            }
        };
        return directive;

        function link(scope, ele, attr) {
            if (attr["required"]) {
                $(elem).wrap("<span zb-required></span>")
            }
            if (attr.hasOwnProperty('type') && attr['type'] !== 'int') {
                scope.type = 2;
            } else {
                scope.type = 1
            }
            if (scope.type === 2) {
                var fraction = scope.$root.systemConfig.dec_place_currency ? scope.$root.systemConfig.dec_place_currency : 0;
                if (attr["fraction"]) {
                    fraction = Number(attr["fraction"]);
                }

                var nStep = "0.";
                var iDecimal = scope.$root.systemConfig.dec_place_currency ? scope.$root.systemConfig.dec_place_currency : 0;
                for (var i = 0; i < iDecimal; i++) {
                    nStep += (i < iDecimal - 1) ? "0" : "1";
                }
                if (attr["step"] && attr["step"] != "0") {
                    nStep = attr["step"];
                }

                ele.find("input[type='number']").attr("step", nStep);

                attr.$observe("step", function (value) {
                    ele.find("input[type='number']").attr("step", value);
                });

                if (attr["ngModel"]) {
                    var startValue = scope.ngModel;
                    if (angular.isNumber(startValue)) {
                        ele.find("input[type='number']").val(startValue ? startValue : null);
                        var txtValue = $filter("number")(startValue, fraction).split(",").join("");

                        ele.find("input[type='text']").val(scope.$root.$groupingNumber(txtValue));
                    } else {
                        scope.ngModel = null;
                        scope.$applyAsync();
                    }
                }

                scope.$watch('ngModel', function (value, oldValue) {
                    var fNumber = parseFloat(value);
                    if (angular.isNumber(fNumber)) {
                        ele.find("input[type='number']").val(fNumber ? fNumber : null);
                        var txtValue = $filter("number")(fNumber, fraction).split(",").join("");
                        ele.find("input[type='text']").val(scope.$root.$groupingNumber(txtValue));
                        scope.ngModel = fNumber ? fNumber : null;
                        scope.$applyAsync();
                    } else {
                        scope.ngModel = null;
                        scope.$applyAsync();
                    }
                });

                ele.find("input[type='number']").bind('input', function (val) {
                    var fNumber = parseFloat(val.currentTarget.value);
                    if (fNumber) {
                        scope.ngModel = parseFloat(val.currentTarget.value);
                    } else {
                        scope.ngModel = null;
                    }
                    scope.$applyAsync();
                });

                ele.find("input[type='text']").bind("focus", function () {
                    $(this).hide();
                    ele.find("input[type='number']").show().focus();
                });

                ele.find("input[type='number']").focusout(function () {
                    $(this).hide();
                    ele.find("input[type='text']").show();
                    var value = Number(ele.find("input[type='number']").val());
                    if (attr["ngModel"]) {
                        if (value) {
                            $parse(attr["ngModel"]).assign(scope, value);
                        }
                        else {
                            $parse(attr["ngModel"]).assign(scope, null);
                        }
                        scope.$apply();
                    }
                    var txtValue = $filter("number")(value, fraction).split(",").join("");

                    ele.find("input[type='text']").val(scope.$root.$groupingNumber(txtValue));
                    if (attr["ngChange"]) {
                        scope.$eval(attr["ngChange"]);
                    }
                });
            }
            else {
                ele.find("input[type='number']").val(scope.ngModel);
                ele.find("input[type='text']").val(scope.ngModel ? scope.$root.$groupingNumber(scope.ngModel) : null);

                ele.find("input[type='text']").bind("focus", function () {
                    $(this).hide();
                    ele.find("input[type='number']").show().focus();
                });

                ele.find("input[type='number']").focusout(function () {
                    $(this).hide();
                    ele.find("input[type='text']").show();
                });

                ele.find("input[type='number']").bind('input', function (val) {
                    scope.ngModel = parseInt(val.currentTarget.value);
                    ele.find("input[type='text']").val(scope.$root.$groupingNumber(val.currentTarget.value));
                    scope.$applyAsync();
                });

                scope.$watch('ngModel', function (val) {
                    if (val) {
                        ele.find("input[type='number']").val(val);
                        ele.find("input[type='text']").val(scope.$root.$groupingNumber(scope.ngModel));
                    }else{
                        ele.find("input[type='number']").val(null);
                        ele.find("input[type='text']").val("");
                    }
                })
            }
        }
    }

})();