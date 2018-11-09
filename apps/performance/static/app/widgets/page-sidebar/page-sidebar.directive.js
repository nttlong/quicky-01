(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('pageSidebar', ["$compile", "templateService", "authenticatedService", pageSidebar]);

    function pageSidebar($compile, templateService, authenticatedService) {
        return {
            restrict: 'E',
            replace: true,
            transclude: {
                siteMap: "?siteMap",
                advancedSearch: "?advancedSearch",
                extendToolbar: "?extendToolbar",
                content: "content"
            },
            scope: {
                fnGen: "=onGen",
                fnAdd: "=onAdd",
                fnEdit: "=onEdit",
                fnDelete: "=onDelete",
                fnSave: "=onSave",
                fnCopy: "=onCopy",
                fnImport: "=onImport",
                fnExport: "=onExport",
                fnPrint: "=onPrint",
                fnAction: "=onAction",
                fnRefresh: "=onRefresh",
                fnSearchPress: "=onSearchPress",
                fnSearchChange: "=onSearchChange",
                listItem: "=source",
                keyField: "@",
                displayField: "@",
                iconField: "@",
                selectedKey: "=",
                reloadOnChange: "=",
                advancedSearch: "=",
                extendToolbar: "=",
                disabled: "=",
                initAuthen: "="
            },
            templateUrl: templateService.getStatic("app/widgets/page-sidebar/page-sidebar.html"),
            link: function ($scope, elem, attr, ctrls, $transclude) {
                var left = $(elem).find(".zb-left");
                var right = $(elem).find(".zb-right");
                var rightContent = $(elem).find(".zb-right .zb-content");
                var btnCollapse = $(elem).find("#btnCollapse");

                var advancedSearch = $(elem).find(".zb-advanced-search");
                var btnAdvancedSearch = $(elem).find("#btnAdvancedSearch");
                var left_ul = $(elem).find(".zb-left-ul");
                var zb_left_thumb_y = $(elem).find(".zb-left-thumb-y");
                var zb_left_rail_y = $(elem).find(".zb-left-rail-y");

                left.on( "mouseenter", function() {
                    zb_left_rail_y.css({
                        "display": "block",
                    })
                  })
                  .on( "mouseleave", function() {
                    zb_left_rail_y.css({
                        "display": "none",
                    })
                });

                if($scope.initAuthen === true){
                    authenticatedService.getPermissionByFunctionId($scope.$root.$$$authoriseFunction.id, function(res){
                        $scope.authorise = res;
                        $scope.$root.$$$authoriseFunction.authorisePermission = res;
                        $scope.$applyAsync();
                    });
                }

                $scope.$watch("listItem", function (v) {
                    if(v && v.length != 0){
                        if(!attr.hasOwnProperty("notAuthentication")){
                            $scope.$root.$$$authoriseFunction.id = v[0].function_id;
                            authenticatedService.getPermissionByFunctionId(v[0].function_id, function(res){
                                $scope.authorise = res;
                                $scope.$root.$$$authoriseFunction.authorisePermission = res;
                                $scope.$applyAsync();
                                zb_left_thumb_y.css({
                                    "height": left_ul.height()
                                })
                                left.scroll(function() {
                                   var scroll = left.scrollTop();
                                    zb_left_rail_y.scrollTop(scroll);
                                });

                            });
                        }
                    }
                    if (!$scope.selectedKey && angular.isArray($scope.listItem) && $scope.listItem.length > 0) {
                        $scope.selectedKey = $scope.listItem[0][$scope.keyField];
                        if(!attr.hasOwnProperty("notAuthentication")){
                            $scope.$root.$$$authoriseFunction.id = $scope.selectedKey;
                            authenticatedService.getPermissionByFunctionId($scope.selectedKey, function(res){
                                $scope.authorise = res;
                                $scope.$root.$$$authoriseFunction.authorisePermission = res;
                                $scope.$applyAsync();
                            });
                        }
                    }
                });

                $scope.isAdvancedSearch = $transclude.isSlotFilled('advancedSearch');
                $scope.showAdvancedSearch = showAdvancedSearch;
                $scope.toggleCollapseMenu = toggleCollapseMenu;
                $scope.checkItemDisabled = checkItemDisabled;
                $scope.$onSelectItem = $onSelectItem;

                $scope.$applyAsync();


                function toggleCollapseMenu() {
                    left.toggleClass("zb-hidden");
                    right.toggleClass("zb-fullscreen");
                    setTimeout(function () {
                        $(window).trigger("resize");
                    }, 300);
                }

                function showAdvancedSearch() {
                    advancedSearch.toggleClass("zb-show");
                    rightContent.toggleClass("show-advanced");
                }

                function checkItemDisabled(func_id){
                    return $scope.disabled && $scope.disabled.includes(func_id) ? true : false;
                }

                function $onSelectItem(key) {
                    if(!$scope.disabled || ($scope.disabled && !$scope.disabled.includes(key))){
                        $scope.selectedKey = key;
                        if(!attr.hasOwnProperty("notAuthentication")){
                            $scope.$root.$$$authoriseFunction.id = $scope.selectedKey;
                        }
                    }

                    if($scope.selectedKey){
                        if(!attr.hasOwnProperty("notAuthentication")){
                            $scope.$root.$$$authoriseFunction.id = $scope.selectedKey;
                            authenticatedService.getPermissionByFunctionId($scope.selectedKey, function(res){
                                $scope.authorise = res;
                                $scope.$root.$$$authoriseFunction.authorisePermission = res;
                                $scope.$applyAsync();
                            });
                        }
                    }else{
                        $scope.fnGen = null;
                        $scope.fnAdd = null;
                        $scope.fnEdit = null;
                        $scope.fnDelete = null;
                        $scope.fnSave = null;
                        $scope.fnCopy = null;
                        $scope.fnImport = null;
                        $scope.fnExport = null;
                        $scope.fnPrint = null;
                        $scope.fnAction = null;
                        $scope.fnRefresh = null;
                        $scope.fnSearchPress = null;
                        $scope.fnSearchChange = null;
                    }

                    $scope.$applyAsync();
                }
            }
        };
    }
})();