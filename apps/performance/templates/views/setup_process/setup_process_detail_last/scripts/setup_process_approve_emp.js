(function (scope) {
    var _view = [
        "${get_app_url('')}/pages/setup_process/setup_process_detail_last/setup_process_approve_emp/employee",
        "${get_app_url('')}/pages/setup_process/setup_process_detail_last/setup_process_approve_emp/department"
    ];
    debugger
    scope.$partialpage = "";
    scope.$parent.$parent.$parent.onSearch = function(val){};
    scope.$parent.$parent.$parent.onAdd = function(){
        alert('onAdd 1');
    };
    scope.$parent.$parent.$parent.onEdit = function(){
        alert('onEdit 1');
    };
    scope.$parent.$parent.$parent.onDelete = function(){
        alert('onDelete 1');
    };
    scope.$parent.$parent.$parent.onImport = function(){
        alert('onImport 1');
    };
    scope.$parent.$parent.$parent.onExport = function(){
        alert('onExport 1');
    };
    scope.$parent.$parent.$parent.onSave = null;

    scope.$$process_id = scope.$parent.$parent.$parent.$parent.$$process_id;
    scope.$$curr_max_approve_level = JSON.parse(JSON.stringify(scope.$parent.$parent.$parent.$parent.$$curr_max_approve_level));

    scope.changeActive = function(event, view){
        if(view == "department"){
            if(scope.$parent.$parent.$parent.$parent.$$is_approve_by_dept && scope.$parent.$parent.$parent.$parent.$$is_approve_by_dept == true)
                scope.$partialpage = _view[1];
        }
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