(function (scope) {
    scope.$parent.$parent.$parent.$parent.detail.onAdd = null;
    scope.$parent.$parent.$parent.$parent.detail.onEdit = null;
    scope.$parent.$parent.$parent.$parent.detail.onSearch = null;
    scope.$parent.$parent.$parent.$parent.detail.onDelete = null;
    scope.$parent.$parent.$parent.$parent.detail.onImport = null;
    scope.$parent.$parent.$parent.$parent.detail.onExport = null;
    scope.$parent.$parent.$parent.$parent.detail.onRefresh = null;
    scope.$parent.$parent.$parent.$parent.detail.onSave = onSave;
    function onSave() {
        alert('onSave');
    };
});