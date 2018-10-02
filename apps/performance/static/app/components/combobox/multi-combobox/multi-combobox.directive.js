(function () {
    'use strict';

    angular.module('ZebraApp.components.combobox')
        .directive('multiCombobox', ["$compile", "templateService", combobox]);

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
                reload: "="
            },
            //template: function(el, attrs) {
            //  return '<div class="switch-container ' + (attrs.color || '') + '"><input type="checkbox" ng-model="ngModel"></div>';
            //}
            templateUrl: templateService.getStatic("app/components/combobox/multi-combobox/multi-combobox.html"),
            //templateUrl: "app/components/input/text/text.html",
            link: function ($scope, elem, attr, ctrl, transclude) {
                $scope.keyField = ($scope.keyField) ? $scope.keyField : "";
                $scope.captionField = ($scope.captionField) ? $scope.captionField : "";
                $scope.title = ($scope.title) ? $scope.title : "";
                $scope.templateFields = ($scope.templateFields) ? $scope.templateFields : [];
                $scope.$deleteSelectedItem = function (item) {
                    if ($scope.$selectedItemDisplay && $scope.$selectedItemDisplay.length > 0) {
                        if ($scope.$cbbConfig) {
                            var check = _.findWhere($scope.$cbbConfig.selected, { [$scope.keyField]: item[$scope.keyField] });
                            //$scope.$cbbConfig.selected = _.reject($scope.$cbbConfig.selected, check);
                            $scope.$cbbConfig.onCheck(null, check, "select");
                        }
                        $scope.ngModel = _.reject($scope.ngModel, function (val) {
                            return val == item[$scope.keyField];
                        });
                        var check = _.findWhere($scope.$selectedItemDisplay, { [$scope.keyField]: item[$scope.keyField] });
                        $scope.$selectedItemDisplay = _.reject($scope.$selectedItemDisplay, check);
                        $scope.$applyAsync();
                    }
                }
                $scope.getValueString = function(){
                    if($scope.$selectedItemDisplay && $scope.$selectedItemDisplay.length > 0)
                        return _.pluck($scope.$selectedItemDisplay, $scope.captionField).join(", ");
                    return "";
                }

                var _control = {
                    setCaption: function () {
                        var placeholder = $(elem).find(".placeholder");
                        var displayValue = $(elem).find(".display-value");

                        //if ($scope.$selectedItem && $scope.$selectedItem[$scope.captionField]) {
                        //    placeholder.hide();
                        //    displayValue.show();
                        //} else {
                        //    placeholder.show();
                        //    displayValue.hide();
                        //}
                    },
                    setValue: function (items) {
                        if ($scope.keyField) {
                            $scope.ngModel = _.pluck(items, $scope.keyField);
                            $scope.$applyAsync();
                        }
                    },
                    setSelectedItem: function (items) {
                        $scope.$selectedItemDisplay = items;
                        $scope.$applyAsync();
                    },
                    clearValue: function () {
                        $scope.ngModel = null;
                        if ($scope.$cbbConfig) {
                            _.map($scope.$cbbConfig.list, function (val) {
                                val['$$$checked'] = false;
                            });
                            $scope.$cbbConfig.checkedAll = false;
                            $scope.$cbbConfig.selected = [];
                        }
                        $scope.$selectedItemDisplay = [];
                        _control.setCaption(null);
                        $scope.$applyAsync();
                    }
                }

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
                    '                <div class="zb-combobox-toolbar" style="display: grid; grid-auto-columns: auto 1fr;">' +
                    '                    <div style="grid-area: 1 / 1 / 1 / 2;width:45px;">' +
                    '                       <div class="checkbox zb-form-checkbox"><label class="custom-checkbox" style="margin-left: 13px;"><input type="checkbox" ng-model="$cbbConfig.checkedAll" ng-click="$cbbConfig.onCheckAll($event, $cbbConfig.list)"><span></span></label></div>' +
                    '                    </div>' +
                    '                    <div style="grid-area: 1 / 2 / 2 / 3">' +
                    '                       <input-text-icon icon="bowtie-icon bowtie-search" icon-align="right" placeholder="{{placeholder}}" on-change="$cbbConfig.onSearchChange" on-click="$cbbConfig.onSearchPress" ng-model="texticon"></input-text-icon>' +
                    '                    </div>' +
                    '                </div>' +
                    '                <div class="zb-combobox-content">' +
                    '                   <div style="display: grid; grid-auto-columns: auto 1fr;" class="zb-combo-list-multi" ng-repeat="$cbbItem in $cbbConfig.list track by $index" ng-class="{active:$cbbConfig._contains($cbbConfig.selected, $cbbItem)}">' +
                    '                   <div style="grid-area: 1 / 1 / 2 / 2;width:40px;border-bottom: 1px solid #ddd;">' +
                    '                       <div class="checkbox zb-form-checkbox"><label class="custom-checkbox" style="margin: 15px;"><input type="checkbox" ng-model="$cbbItem.$$$checked" ng-click="$cbbConfig.onCheck($event, $cbbItem)"><span></span></label></div>' +
                    '                   </div>' +
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

                var htmlTemplate = $('<div class="zb-list-common" style="grid-area: 1 / 2 / 2 / 3;" ng-click="$cbbConfig.onSelect($event, $cbbItem)"></div>');
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
                    }
                });

                function drawCombobox(htmlTemplate) {
                    dialogTemplate = dialogTemplate.replace("<<template>>", htmlTemplate);
                    var $dialog = $(dialogTemplate);
                    var __init__ = 0;

                    $(elem).find(".zb-open-modal").bind("click", function () {
                        __init__ += 1;
                        $dialog.appendTo("body");
                        $dialog.modal({ backdrop: 'static', keyboard: true });

                        if (!$scope.$cbbConfig || ($scope.hasOwnProperty('reload') && $scope.reload === true)) {
                            var fnLoadData = function (pgIdx, txtSearch) {
                                if (angular.isFunction($scope.loadData)) {
                                    ($scope.loadData)($scope, function (result) {
                                        $scope.$cbbConfig.list = (result && result.data) ? result.data : [];
                                        // var selected = []
                                        // if ($scope.$cbbConfig.selected && $scope.$cbbConfig.selected.length > 0) {
                                        //     selected = _.pluck($scope.$cbbConfig.selected, $scope.keyField);
                                        // }
                                        _.map($scope.$cbbConfig.list, function (val) {
                                            if ($scope.ngModel && $scope.ngModel.length > 0) {
                                                if ($scope.ngModel.includes(val[$scope.keyField]))
                                                    val['$$$checked'] = true;
                                                else {
                                                    val['$$$checked'] = false;
                                                }
                                            } else {
                                                val['$$$checked'] = false;
                                            }
                                        });
                                        $scope.$cbbConfig.numberItems = (result && result.recordsTotal) ? result.recordsTotal : 0;
                                        $scope.$applyAsync();
                                    }, pgIdx, txtSearch, $scope.$params);
                                }
                            }

                            $scope.$cbbConfig = {
                                list: [], //$scope.dataSource ? $scope.dataSource : [],
                                checkedAll: false,
                                selected: [],
                                //setCheckedInit: function (source) {
                                //    _.each($scope.$cbbConfig.list, function (val) {
                                //        var objSearch = {};
                                //        objSearch[$scope.keyField] = value[$scope.keyField];
                                //        if (_.findWhere(source, objSearch))
                                //            val['$$$checked'] = true;
                                //    })
                                //},
                                setSeletedValue: function (item) {
                                    var check = _.findWhere($scope.$cbbConfig.selected, { [$scope.keyField]: item[$scope.keyField]});
                                    if (check) {
                                        $scope.$cbbConfig.selected = _.reject($scope.$cbbConfig.selected, check);
                                    } else {
                                        $scope.$cbbConfig.selected = _.uniq(_.union($scope.$cbbConfig.selected, [item]), false, _.property($scope.keyField));
                                    }
                                    if ($scope.$cbbConfig.list.length !== $scope.$cbbConfig.selected.length) {
                                        $scope.$cbbConfig.checkedAll = false;
                                    } else {
                                        $scope.$cbbConfig.checkedAll = true;
                                    }
                                    $scope.$applyAsync();
                                },
                                _contains: function (source, value) {
                                    return _.findWhere(source, { [$scope.keyField]: value[$scope.keyField] }) ? true : false;
                                },
                                onCheckAll: function ($event, items) {
                                    if ($scope.$cbbConfig.checkedAll) {
                                        $scope.$cbbConfig.selected = [];
                                        _.each(items, function (val) {
                                            val['$$$checked'] = true;
                                            $scope.$cbbConfig.selected.push(val);
                                        });
                                    } else {
                                        _.each(items, function (val) {
                                            val['$$$checked'] = false;
                                        });
                                        $scope.$cbbConfig.selected = [];
                                    }
                                    $scope.$applyAsync();
                                },
                                onCheck: function ($event, item, select) {
                                    if (select)
                                        item.$$$checked = item.$$$checked ? false : true;
                                    $scope.$cbbConfig.setSeletedValue(item);
                                },
                                onSelect: function ($event, item) {
                                    $scope.$cbbConfig.onCheck($event, item, "select");
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

                                onAccept: function (items) {
                                    items = items ? items : $scope.$cbbConfig.selected;
                                    if (items) {
                                        _control.setValue(items);
                                        _control.setSelectedItem(items);

                                        if (angular.isFunction($scope.onAccept)) {
                                            ($scope.onAccept)(items);
                                        }
                                    }
                                    $dialog.modal("hide");
                                }
                            }

                            if (__init__ == 1) {
                                //_.map($scope.$selectedItemDisplay, function (val) {
                                //    return val['$$$checked'] = true;
                                //});
                                $scope.$cbbConfig.selected = JSON.parse(JSON.stringify($scope.$selectedItemDisplay));
                            }
                            $scope.$applyAsync();
                            fnLoadData();
                        }else{
                            if($scope.$cbbConfig){
                                $scope.$cbbConfig.selected = [];
                                _.map($scope.$cbbConfig.list, function (val) {
                                    if ($scope.ngModel && $scope.ngModel.length > 0) {
                                        if ($scope.ngModel.includes(val[$scope.keyField])){
                                            val['$$$checked'] = true;
                                            $scope.$cbbConfig.selected.push(val);
                                        }
                                        else {
                                            val['$$$checked'] = false;
                                        }
                                    } else {
                                        val['$$$checked'] = false;
                                    }
                                });
                                $scope.$applyAsync();
                            }
                        }
                    });
                    $dialog.find(".zb-close-modal").bind("click", function () {
                        $dialog.modal("hide");
                    });
                    $compile($dialog)($scope);
                }

                $scope.$watch("initData", function (val) {
                    $scope.$selectedItemDisplay = val;
                    _control.setCaption();
                    $scope.$applyAsync();
                });
            }
        };
    }
})();