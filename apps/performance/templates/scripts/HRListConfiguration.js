(function (scope) {
    var _view = [
        "${get_app_url('')}/pages/HRListConfiguration/company",
        "${get_app_url('')}/pages/HRListConfiguration/department"
    ];
    scope.$partialpage = "";
    scope.onSearch = function(){};
    scope.onAdd = function(){};
    scope.onEdit = function(){};
    scope.onDelete = function(){};
    scope.onImport = function(){};
    scope.onExport = function(){};

    scope.changeActive = function(event, view){
        if(view == "department")
            scope.$partialpage = _view[1];
        else
            scope.$partialpage = _view[0];
        $('.hcs-tab-info').find('.active').removeClass('active');
        $(event.target).closest('div').addClass('active');
        scope.$applyAsync();
    }

    scope.onFilter = function () {
        $("#filter").height(40);
    }

    init();

    function init() {
        scope.$partialpage = _view[0];
    }
});