(function () {
    'use strict';

    angular.module('ZebraApp.widgets')
        .directive('headerPage', ["$compile", headerPage]);

    function headerPage($compile) {
        return {
            restrict: 'E',
            replace: true,
            transclude: {
                siteMap: "?siteMap",
                extendToolbar: "?toolbar",
                content: "?content"
            },
            scope: {
                fnAdd: "=onAdd",
                fnEdit: "=onEdit",
                fnDelete: "=onDelete",
                fnSave: "=onSave",
                fnImport: "=onImport",
                fnExport: "=onExport",
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
            //templateUrl: "app/widgets/page-sidebar/page-sidebar.html",
            template: `
            <div class="zb-page-sidebar hcs-page-sidebar-custom">
                <div class="zb-right hcs-right-custom">
                    <div class="zb-top">
                        <div class="zb-left-content">
                            <button ng-click="toggleCollapseMenu()" class="zb-btn zb-btn-blue zb-btn-collapse"
                                style="opacity: 0">
                                <i class="bowtie-icon bowtie-menu"></i>
                            </button>
                            <div ng-transclude="siteMap" class="zb-sitemap"></div>
                        </div>
                        <div class="zb-right-content" ng-transclude="extendToolbar">
                            
                        </div>
                    </div>
                </div>
            </div>
            `,
            link: function ($scope, elem, attr, ctrls, $transclude) {
                debugger
                console.log($scope)
                var left = $(elem).find(".zb-left");
                var right = $(elem).find(".zb-right");
                var rightContent = $(elem).find(".zb-right .zb-content");
                var btnCollapse = $(elem).find("#btnCollapse");

                var advancedSearch = $(elem).find(".zb-advanced-search");
                var btnAdvancedSearch = $(elem).find("#btnAdvancedSearch");

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