(function () {
    'use strict';
    angular
        .module('authenticatedModule')
        .factory("authenticatedService", authenticatedService);

    window.set_authenticated_permission_service = function(url){
        fac.path = url;
    }
    var fac = {
        path: ""
    }
    function authenticatedService() {

        fac.getPermissionByFunctionId = getPermissionByFunctionId;

        function getPermissionByFunctionId(funcId, callback){
            services.api(fac.path)
            .data({
                function_id : funcId
            })
            .done()
            .then(function (res) {
                callback(res);
            })
        }

        return fac;
    }
})();