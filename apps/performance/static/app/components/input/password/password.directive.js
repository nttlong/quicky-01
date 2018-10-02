(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputPassword', password);

    password.$inject = ['$window'];
    
    function password ($window) {
        // Usage:
        //     <input-password></input-password>
        // Creates:
        // 
        var directive = {
            restrict: 'E',
            replace: true,
            transclude: true,
            scope: {
                result: "=",
                ngDisabled: "="
            },
            template: '<input type="password" ng-disabled="ngDisabled" class="form-control zb-form-input"/>',
            link: link
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs["required"]) {
                $(element).wrap("<span zb-required></span>")
            }
        }

        
    }

})();