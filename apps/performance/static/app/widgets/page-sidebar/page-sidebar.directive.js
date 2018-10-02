(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('pageSidebar', ["$compile", "templateService", pageSidebar]);

    function pageSidebar($compile, templateService) {
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
                fnAdd: "=onAdd",
                fnEdit: "=onEdit",
                fnDelete: "=onDelete",
                fnSave: "=onSave",
                fnImport: "=onImport",
                fnExport: "=onExport",
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
                extendToolbar: "="
            },
            templateUrl: templateService.getStatic("app/widgets/page-sidebar/page-sidebar.html"),
            link: function ($scope, elem, attr, ctrls, $transclude) {
                console.log($scope)
                var left = $(elem).find(".zb-left");
                var right = $(elem).find(".zb-right");
                var rightContent = $(elem).find(".zb-right .zb-content");
                var btnCollapse = $(elem).find("#btnCollapse");

                var advancedSearch = $(elem).find(".zb-advanced-search");
                var btnAdvancedSearch = $(elem).find("#btnAdvancedSearch");

                $scope.$watch("listItem", function (v) {
                    if (!$scope.selectedKey && angular.isArray($scope.listItem) && $scope.listItem.length > 0) {
                        $scope.selectedKey = $scope.listItem[0][$scope.keyField];
                    }
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

                    //if ($scope.reloadOnChange) {
                    //    $scope.fnAdd = null;
                    //    $scope.fnEdit = null;
                    //    $scope.fnDelete = null;
                    //    $scope.fnSave = null;
                    //    $scope.fnImport = null;
                    //    $scope.fnExport = null;
                    //    $scope.fnSearchPress = null;
                    //    $scope.fnSearchChange = null;
                    //}

                    $scope.$applyAsync();
                }
            }
        };
    }
})();