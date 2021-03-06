(function () {
    'use strict';

    angular.module('ZebraApp.components.combobox')
        .directive('combobox', ["$compile", "templateService", combobox]);

    /** @ngInject */
    function combobox($compile, templateService) {
        return {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                loadData: "=",
                //dataSource: "=source",
                title: "@",
                onSelect: "=",
                onAccept: "=",

                /*begin search*/
                onSearchChange: "=",
                onSearchPress: "=",
                /*end search*/

                /*begin pagination*/
                paging: "=",
                //onPaging: "=",
                //numberItems: "@",
                numberOnPage: "=",
                pageIndex: "=",
                /*end pagination*/

                closeOnSelect: "@",

                placeholder: "@",
                ngModel: "=",
                /*Field lấy giá trị cho combobox*/
                keyField: "@",
                /*Field hiển thị trên combobox*/
                captionField: "@",
                /*Caption hiển thị khi lần đầu loadCombobox*/
                initData: "=",
                params: "=",
                ngDisabled: "=",
                templateFields: "=",
                /*Reload data khi nhấn button mở combobox*/
                reload: "=",
                ngRequired: "@",
                ngChange: "="
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: templateService.getStatic("app/components/combobox/combobox/combobox.html"),
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrl, transclude) {
                $scope.keyField = ($scope.keyField) ? $scope.keyField : "";
                $scope.captionField = ($scope.captionField) ? $scope.captionField : "";
                $scope.title = ($scope.title) ? $scope.title : "";
                $scope.templateFields = ($scope.templateFields) ? $scope.templateFields : [];
                if($scope.ngRequired === 'true' || (attr["required"] && (!$scope.ngRequired))){
                  $(elem).wrap("<span zb-required></span>")
                }
                var _control = {
                    setCaption: function () {
                        var placeholder = $(elem).find(".placeholder");
                        var displayValue = $(elem).find(".display-value");
                        if ($scope.$selectedItem && $scope.$selectedItem[$scope.captionField]) {
                            placeholder.hide();
                            displayValue.show();
                        } else {
                            placeholder.show();
                            displayValue.hide();
                        }
                    },
                    applyCaption: function (item) {
                        if ($scope.captionField) {
                            $scope.$selectedItem = item;
                            if (item && item[$scope.captionField]) {
                                _control.setCaption(item[$scope.captionField]);
                            } else {
                                _control.setCaption(null);
                            }
                        }
                    },
                    setValue: function (item) {
                        if ($scope.keyField) {
                            $scope.ngModel = item[$scope.keyField];
                            $scope.$applyAsync();
                        }
                    },
                    setSelectedItem: function (item) {
                        $scope.$selectedItem = item;
                        $scope.$applyAsync();
                    },
                    clearValue: function () {
                        $scope.ngModel = null;
                        _control.setCaption(null);
                        $scope.$applyAsync();
                    }
                }

                $(elem).find('input[type=text]').bind('keyup', function(e){
                    if($scope.$selectedItem){
                        if(e.keyCode === 8){
                            if($scope.$selectedItem[$scope.captionField] != e.currentTarget.value){
                                _control.clearValue();
                            }
                        }
                    }
                })

                var dialogTemplate = '' +
                    '<div class="zb-modal-combobox modal fade" role="dialog" tabindex="-1">' +
                    '    <div class="modal-dialog modal-dialog-one-col">' +
                    '        <div class="modal-content">' +
                    '            <div class="modal-header">' +
                    '                <div class="left-content pull-left">' +
                    '                    <span class="modal-title">{{title}}</span>' +
                    '                </div>' +
                    '                <div class="right-content pull-right">' +
                    '                    <button type="button" class="close zb-close-modal"><i class="bowtie-icon bowtie-navigate-close"></i></button>' +
                    '                </div>' +
                    '            </div>' +
                    '            <div class="modal-body">' +
                    '                <div class="zb-combobox-toolbar">' +
                    '                    <input-text-icon icon="bowtie-icon bowtie-search" icon-align="right" placeholder="{{placeholder}}" on-change="$cbbConfig.onSearchChange" on-click="$cbbConfig.onSearchPress" ng-model="texticon"></input-text-icon>' +
                    '                </div>' +
                    '                <div class="zb-combobox-content">' +
                    '                   <div class="zb-combo-list" ng-repeat="$cbbItem in $cbbConfig.list" ng-click="$cbbConfig.onSelect($event, $cbbItem)">' +
                    '                     <<template>>' +
                    '                   </div>' +
                    '                </div>' +
                    '            </div>' +
                    '            <div class="modal-footer">' +
                    '                <div class="left-content pull-left" ng-if="$cbbConfig.isPaging">' +
                    '                    <pagination class="zb-combobox-footer" items="$cbbConfig.numberItems" items-on-page="$cbbConfig.numberOnPage" current-page="$cbbConfig.pageIndex" on-page-click="$cbbConfig.onPaging"/>' +
                    '                </div>' +
                    '                <div class="right-content pull-right">' +
                    '                    <button ng-click="$cbbConfig.onAccept()"><i class="bowtie-icon bowtie-check-light"></i></button>' +
                    '                </div>' +
                    '            </div>' +
                    '        </div>' +
                    '    </div>' +
                    '</div>';

                // var htmlTemplate = $(elem).find(".zb-combobox-template").html();
                // var keys = htmlTemplate.match(/(\##.*?\##)/gm);
                // $.each(keys, function(i, v) {
                //     var key = v.split("##").join("");
                //     var retKey = "{{$cbbItem." + key + "}}";
                //     htmlTemplate = htmlTemplate.split(v).join(retKey);
                // });

                var htmlTemplate = $('<div class="zb-list-common"></div>');
                var compiled = false;
                $scope.$watch("templateFields", function (val) {
                    if (angular.isArray(val) && val.length > 0) {
                        var group1 = $("<div></div");
                        if (val.length >= 1) {
                            var field = (typeof (val[0]) == "string") ? val[0] : val[0]["data"];
                            var html = '<span class="zb-list-title">{{$cbbItem.' + field + ' ##Format##}}</span>'
                            if (val[0].hasOwnProperty('format') && val[0].hasOwnProperty('format')) {
                                html = html.replace("##Format##", " | " + val[0]['format']);
                            } else {
                                html = html.replace("##Format##", "");
                            }
                            group1.append(html);
                        }
                        var group2 = $("<div></div");
                        if (val.length >= 2) {
                            var field2 = (typeof (val[1]) == "string") ? val[1] : val[1]["data"];
                            var html = '<span class="zb-list-description">{{$cbbItem.' + field2 + ' ##Format##}}</span>';
                            if (val[1].hasOwnProperty('format') && val[1].hasOwnProperty('format')) {
                                html = html.replace("##Format##", " | " + val[1]['format']);
                            } else {
                                html = html.replace("##Format##", "");
                            }
                            group2.append(html);
                        }
                        if (val.length >= 3) {
                            var field3 = (typeof (val[2]) == "string") ? val[2] : val[2]["data"];
                            var html = '<span class="zb-list-info">{{$cbbItem.' + field3 + ' ##Format##}}</span>';
                            if (val[2].hasOwnProperty('format') && val[2].hasOwnProperty('format')) {
                                html = html.replace("##Format##", " | " + val[2]['format']);
                            } else {
                                html = html.replace("##Format##", "");
                            }
                            group1.append(html);
                        }
                        if (val.length >= 4) {
                            var field4 = (typeof (val[3]) == "string") ? val[3] : val[3]["data"];
                            var html = '<span class="zb-list-number">{{$cbbItem.' + field4 + ' ##Format##}}</span>';
                            if (val[3].hasOwnProperty('format') && val[3].hasOwnProperty('format')) {
                                html = html.replace("##Format##", " | " + val[3]['format']);
                            } else {
                                html = html.replace("##Format##", "");
                            }
                            group2.append(html);
                        }
                        htmlTemplate.append(group1);
                        if (val.length >= 2) {
                            htmlTemplate.append(group2);
                        }

                        if (!compiled) {
                            compiled = true;
                            drawCombobox(($("<div></div").append(htmlTemplate)).html());
                        }
                        //$compile($dialog)($scope);
                    }
                });

                function drawCombobox(htmlTemplate) {
                    dialogTemplate = dialogTemplate.replace("<<template>>", htmlTemplate);
                    var $dialog = $(dialogTemplate);

                    $(elem).find(".zb-open-modal").bind("click", function () {
                        $dialog.appendTo("body");
                        $dialog.modal({ backdrop: 'static', keyboard: true });

                        if (!$scope.$cbbConfig || ($scope.hasOwnProperty('reload') && $scope.reload === true)) {
                            var fnLoadData = function (pgIdx, txtSearch) {
                                if (angular.isFunction($scope.loadData)) {
                                    ($scope.loadData)($scope, function (result) {
                                        $scope.$cbbConfig.list = (result && result.data) ? result.data : [];
                                        $scope.$cbbConfig.numberItems = (result && result.recordsTotal) ? result.recordsTotal : 0;
                                        $scope.$applyAsync();
                                    }, pgIdx, txtSearch, $scope.$params);
                                }
                            }

                            $scope.$cbbConfig = {
                                list: [], //$scope.dataSource ? $scope.dataSource : [],
                                onSelect: function ($event, item) {
                                    var currElem = $($event.target).closest(".zb-combo-list");
                                    currElem.siblings().removeClass("zb-combo-selected");
                                    currElem.addClass("zb-combo-selected");
                                    if (angular.isFunction($scope.onSelect)) {
                                        ($scope.onSelect)(item);
                                    }
                                    _control.setSelectedItem(item);

                                    if (!$scope.closeOnSelect || $scope.closeOnSelect.toLowerCase() != "false") {
                                        $scope.$cbbConfig.onAccept(item);
                                        $dialog.modal("hide");
                                    }
                                },
                                onSearchChange: function (txtSearch) {
                                    if ($scope.onSearchChange) {
                                        $scope.txtSearch = txtSearch;
                                        $scope.$applyAsync()
                                        fnLoadData($scope.currPageIndex, $scope.txtSearch);
                                    }
                                },
                                onSearchPress: function (txtSearch) {
                                    if ($scope.onSearchPress) {
                                        $scope.txtSearch = txtSearch;
                                        $scope.$applyAsync()
                                        fnLoadData($scope.currPageIndex, $scope.txtSearch);
                                    }
                                },

                                isPaging: $scope.paging ? true : false,
                                onPaging: function (pgIdx) {
                                    $scope.currPageIndex = pgIdx;
                                    $scope.$applyAsync()
                                    fnLoadData($scope.currPageIndex, $scope.txtSearch);
                                },
                                numberItems: 0,
                                numberOnPage: $scope.numberOnPage ? $scope.numberOnPage : 30,
                                pageIndex: $scope.pageIndex ? $scope.pageIndex : 1,

                                onAccept: function (item) {
                                    item = item ? item : $scope.$selectedItem;
                                    if (item) {
                                        _control.setValue(item);
                                        _control.applyCaption(item);

                                        if (angular.isFunction($scope.onAccept)) {
                                            ($scope.onAccept)(item);
                                        }
                                    }
                                    $dialog.modal("hide");
                                }
                            }
                            $scope.$applyAsync();
                            fnLoadData();
                        }
                    });
                    $dialog.find(".zb-close-modal").bind("click", function () {
                        $dialog.modal("hide");
                    });
                    $compile($dialog)($scope);
                }

                $scope.$watch("initData", function (val) {
                    $scope.$selectedItem = val;
                    _control.setCaption();
                    $scope.$applyAsync();
                });

                $scope.$watch("ngModel", function(val){
                    if(!val){
                        $scope.initData = null;
                        _control.applyCaption(null);
                    }
                    if (angular.isFunction($scope.ngChange)) {
                        ($scope.ngChange)(val);
                    }
                })
            }
        };
    }
})();