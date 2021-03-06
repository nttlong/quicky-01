angular.module('ZebraApp.components', [
    'ui.select',
    'ui.bootstrap',
    'ui.bootstrap.tpls',
    'ui.bootstrap.collapse',
    'ZebraApp.components.inputs',
    'ZebraApp.components.outputs',
    'ZebraApp.components.tables',
    'ZebraApp.components.trees',
    'ZebraApp.components.combobox',
    'ZebraApp.components.lists'
])
.run(['$templateCache', function ($templateCache) {
    $templateCache.put('app/components/input/checkbox/checkbox.html', '<div class="checkbox zb-form-checkbox"><label class="custom-checkbox" ng-disabled="ngDisabled"><input type="checkbox" ng-disabled="ngDisabled" ng-model="model"><span>{{caption}}</span></label></div>');
    $templateCache.put('app/components/input/datepicker/datepicker.html', '<span class="input-group zb-form-date-picker"><input type="text" class="form-control" ng-disabled="ngDisabled" uib-datepicker-popup="{{format}}" datepicker-options="options" ng-model="dt" is-open="opened" close-text="Close" alt-input-formats="altInputFormats" show-button-bar="true" placeholder="{{placeholder}}"><span class="input-group-btn"><button type="button" ng-disabled="ngDisabled" class="btn btn-default"><i class="sap-icon sap-appointment-2"></i></button></span></span>');
    //$templateCache.put('app/components/input/select/select.html', '<div ng-controller="SelectpickerPanelCtrl as selectpickerVm" ng-disabled="ngDisabled" class="zb-form-select"><ui-select ng-model="selectedItem.selected" class="btn-group bootstrap-select form-control" ng-disabled="ngDisabled" append-to-body="false" search-enabled="true" title="{{$select.selected.__fieldCaption}}"><ui-select-match placeholder="{{placeholder}}">{{$select.selected.__fieldCaption}}</ui-select-match><ui-select-choices repeat="searchItem in selectWithSearchItems | filter: $select.search"><span ng-bind-html="searchItem.__fieldCaption" title="{{searchItem.__fieldCaption}}"></span></ui-select-choices></ui-select></div>');
    $templateCache.put('app/components/table/table-data/table-data.html', '<table class="display zb-data-table responsive nowrap" cellspacing="0"></table>');
    $templateCache.put('app/components/tree/tree/tree.html', '<div class="zb-tree"><div id="tree"></div></div>');
    $templateCache.put('app/components/tree/tree-table/tree-table.html', '<div id="scrolling_table" class="dataTables_scroll"><table class="zb-data-table responsive dataTable" id="treetable"><thead><tr><th class="fixed freeze" ng-if="multiSelect"><span role="checkbox" class="zb-tree-table-checkall fancytree-checkbox"></span></th><th class="zb-tree-table-th fixed freeze">{{displayName}}</th><th ng-repeat="f in fields" style="min-width:{{f.width ? f.width : \'auto\'}}" class="fixed freeze_vertical {{f.width ? \'\' : \'zb-tree-table-nowrap\'}} {{f.className ? f.className : \'\'}}">{{f.title}}</th></tr></thead><tbody><tr class="odd"><td class="fixed freeze_horizontal zb-tree-table-checkbox" ng-if="multiSelect"></td><td class="fixed freeze_horizontal zb-tree-table-nowrap"></td><td ng-repeat="f in fields"></td></tr></tbody></table></div>');
}]);



