(function (scope) {
    setTimeout(function(){
        var tabNotification = $('#tabNotification');
        var tabConfirmation = $('#tabConfirmation');
        // var _collapseNotify = collapse(tabNotification.find('.zb-content'));
        // var _collapseConfirm = collapse(tabConfirmation.find('zb-content'));

        function collapse(ele) {
            if (ele.find('.zb-content').is(":hidden")) {
                ele.find(".zb-header-icon i").addClass("zb-icon-up");
                ele.find(".zb-header-icon i").removeClass("zb-icon-down");
            } else {
                ele.find(".zb-header-icon i").removeClass("zb-icon-up");
                ele.find(".zb-header-icon i").addClass("zb-icon-down");
            }
            var toggle = ele.find('.zb-content').slideToggle(300);
        }
        $(document).ready(function(){
            tabNotification.find('.zb-header-icon i').bind("click", function(){
                collapse(tabNotification);
            });
            tabNotification.find(".zb-header-title").bind("click", function(){
                collapse(tabNotification);
            });
        })

        $(document).ready(function(){
            tabConfirmation.find('.zb-header-icon i').bind("click", function(){
                collapse(tabConfirmation);
            });
            tabConfirmation.find(".zb-header-title").bind("click", function(){
                collapse(tabConfirmation);
            });
        });
    }, 500)


    scope.onSave = function(){
        
    }

    scope.reloadData = function (){
        var config = scope.$$table.$$tableConfig;
        _tableData(config.iPage, config.iPageLength, config.orderBy, config.SearchText, config.fnReloadData);
    }

    scope.onImport = function(){
        
    }

    scope.onExport = function(){
        
    }

    scope.onRefresh = function(){
        scope.reloadData();
    }

    init();

    function init() {
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
    }

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
        {
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        }else{
            window.location.href = '#page=' + scope.$root.$extension.TripleDES.encrypt(data['page']);
        }
    });
});