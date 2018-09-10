(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputNumber', inputNumber);

    inputNumber.$inject = ['$window', "$parse", "$filter", "$locale"];
    
    function inputNumber($window, $parse, $filter, $locale) {
        // Usage:
        //     <input-number></input-number>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'ECA',
            template: template(),
            scope: {
                ngModel: "=",
                ngChange: "&"
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
                ele.find("input[type='text']").val(scope.ngModel ? scope.ngModel.toString() : null);

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
                    ele.find("input[type='text']").val(val.currentTarget.value);
                    scope.$applyAsync();
                });

                scope.$watch('ngModel', function (val) {
                    if (val) {
                        ele.find("input[type='number']").val(val);
                        ele.find("input[type='text']").val(val.toString());
                    }else{
                        ele.find("input[type='number']").val(null);
                        ele.find("input[type='text']").val("");
                    }
                })
            }
        }

        function template() {
            return `
                <div class="form-control zb-form-input" style='overflow-y:hidden;margin-top:0;margin-bottom:0;display: block'>
                    <input type="text" style='outline:none;width:100%;height: 100%;border:none;-webkit-appearance:none;text-align:right' />
                    <input type="number" style='outline:none;width:100%;height: 100%;border:none;-webkit-appearance:none;display:none' />
                </div>
                `;
        }
    }

})();