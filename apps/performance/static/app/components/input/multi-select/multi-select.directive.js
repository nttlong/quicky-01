(function() {
    'use strict';

    angular
        .module('ZebraApp.components.inputs')
        .directive('inputMultiSelect', inputMultiSelect)
        .controller('SelectpickerMultiPanelCtrl', SelectpickerMultiPanelCtrl);

    inputMultiSelect.$inject = ['$window'];

    function SelectpickerMultiPanelCtrl($scope, $sce) {

    }

    function inputMultiSelect ($window) {
        // Usage:
        //     <input-multi-select></input-multi-select>
        // Creates:
        // 
        var directive = {
            link: link,
            restrict: 'E',
            controller: SelectpickerMultiPanelCtrl,
            template: template(),
            scope: {
                list: "=",
                ngModel: "=",
                placeholder: "@",
                fieldValue: "@value",
                fieldCaption: "@caption",
                ngDisabled: "=",
                ngChange: "="
            }
        };
        return directive;

        function link(scope, element, attrs) {
            if (attrs.hasOwnProperty('required')) {
                $(element).wrap("<span zb-required></span>")
            }

            var _init_ = null;
            var _flag_ = false;

            function getDisplayString(){
                if(scope.ngModel && scope.ngModel.length > 0)
                {
                    var filter = _.pluck(_.filter(scope.list, function(val){
                        if(scope.ngModel.includes(val[scope.fieldValue]))
                            return true;
                    }), scope.fieldCaption);
                    return filter.join(", ");
                }
                return ""
            }
            scope.$watch('list', function(val){
                if(val){
                    var ctrl = $(element.find('.zb-input-multi-select-component')).SumoSelect({
                        captionFormat: getDisplayString(),
                        searchText: "",
                        placeholder: scope.placeholder ? scope.placeholder : "",
                        search: true
                    });
                    var _control = $(element.find('.zb-input-multi-select-component'))[0].sumo;
                    _.each(val, function(elm, index){
                        _control.add(elm[scope.fieldValue], elm[scope.fieldCaption]);
                    });
                    if(_init_ && !_flag_)
                    {
                        _flag_ = true;
                        _init_();
                    }
                }
            });
            scope.$watch('ngModel', function(val){
                if(val && val.length > 0){
                    if(!scope.dt)
                        scope.dt = val;
                }
            })
            scope.$watch('dt', function(val){
                if(val){
                    if(!_init_)
                    {
                        _init_ = function(){
                            var _dataList = JSON.parse(JSON.stringify(val));
                            var ctrl = $(element.find('.zb-input-multi-select-component'))[0].sumo;
                            _.each(_dataList, function(val){
                                ctrl.selectItem(val.toString());
                            });
                        }
                    }else{
                        var _list = []
                        _.each(val, function(v){
                            var rs = _.find(scope.list, function(e){
                                return e[scope.fieldValue] == v;
                            })
                            if(rs)
                                _list.push(rs[scope.fieldValue]);
                        })
                        scope.ngModel = _list;
                    }
                }
            })
            scope.setValue = function(){
                var _list = [];
                _.each(scope.dt, function(val){
                    var rs = _.find(scope.list, function(e){
                        return e[scope.fieldValue] == val;
                    })
                    if(rs)
                        _list.push(rs[scope.fieldValue]);
                })
                scope.ngModel = _list;
                var ctrl = $(element.find('.zb-input-multi-select-component'));
                ctrl[0].sumo.setTextCustom(getDisplayString());
            };
        }

        function template() {
            return ''
                + '<select multiple="multiple" ng-click="setValue()" ng-model="dt" class="zb-input-multi-select-component">'
                + '</select>';
        }
    }

})();