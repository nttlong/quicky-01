(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('headerPage', ["$compile", "templateService", "authenticatedService", headerPage]);

    function headerPage($compile, templateService, authenticatedService) {
        return {
            restrict: 'E',
            replace: true,
            transclude: {
                siteMap: "?siteMap",
                extendToolbar: "?extendToolbar",
                content: "?content"
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
                disabled: "="
            },
            //templateUrl: "app/widgets/page-sidebar/page-sidebar.html",
            templateUrl: templateService.getStatic("app/widgets/header-page/header-page.html"),
            link: function ($scope, elem, attr, ctrls, $transclude) {
                debugger
                var left = $(elem).find(".zb-left");
                var right = $(elem).find(".zb-right");
                var rightContent = $(elem).find(".zb-right .zb-content");
                var btnCollapse = $(elem).find("#btnCollapse");

                var advancedSearch = $(elem).find(".zb-advanced-search");
                var btnAdvancedSearch = $(elem).find("#btnAdvancedSearch");

                $scope.$watch("selectedKey", function (v) {
                    authenticatedService.getPermissionByFunctionId(v, function(res){
                        $scope.authorise = res;
                        $scope.$applyAsync();
                    });
                });

                $scope.isAdvancedSearch = $transclude.isSlotFilled('advancedSearch');
                $scope.showAdvancedSearch = showAdvancedSearch;
                $scope.toggleCollapseMenu = toggleCollapseMenu;
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

                function $onSelectItem(key) {
                    $scope.selectedKey = key;

                    if ($scope.reloadOnChange) {
                        $scope.fnAdd = null;
                        $scope.fnEdit = null;
                        $scope.fnDelete = null;
                        $scope.fnSave = null;
                        $scope.fnImport = null;
                        $scope.fnExport = null;
                        $scope.fnSearchPress = null;
                        $scope.fnSearchChange = null;
                    }

                    $scope.$applyAsync();
                }
            }
        };
    }
})();