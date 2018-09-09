var libs_directives;
(function (libs_directives) {
    libs_directives._module.directive('bAgGrid', ["$parse", function ($parse) {

        return {
        restrict: "CEA",
        replace: true,
        template: function(){
            return "<div></div>"
        },
        link: function (scope, ele, attr) {
            var cmp ={}
            var gEle=undefined;
            if(attr.id){
                $parse(attr.id).assign(scope,cmp);
            }
            var dataSource = {
                rowCount: null,
                getRows: function (params) {
                    pageIndex=params.endRow/100 -1;
                    if(attr.onLoadData){
                        var fn= scope.$eval(attr.onLoadData);
                        if(angular.isFunction(fn)){
                            var sender = {
                                params:{
                                    filter:params.filterModel,
                                    sort:params.sortModel,
                                    pageIndex:pageIndex,
                                    pageSize:params.endRow-params.startRow,
                                },
                                done:function(res){
                                    params.successCallback(res.items, res.total_items);
                                }
                            }
                            fn(sender)
                        }
                    }
    
                }
            };
            var gridOptions = {
                columnDefs: [],
                enableServerSideFilter: true,
                floatingFilter:false,
                enableServerSideSorting: true,
                enableColResize: true,
                rowBuffer: 0,
                debug: true,
                rowSelection: 'multiple',
                rowDeselection: true,
                rowModelType: 'infinite',
                paginationPageSize: 20,
                cacheOverflowSize: 2,
                maxConcurrentDatasourceRequests: 2,
                infiniteInitialRowCount: 1,
                maxBlocksInCache: 2,
                onGridReady: function(params) {
                    params.api.sizeColumnsToFit();
                    params.api.setDatasource(dataSource);
                    var h=ele.height();
                    function watchHeight(){
                        var r=ele.height()
                        if(h!=r){
                            h=r;
                            fixHeight(r);

                        }
                        setTimeout(watchHeight,100);
                    }
                    
                    function fixHeight(r){
                        gEle.css({
                            height:r
                        })

                        params.api.sizeColumnsToFit();
                    }
                    watchHeight();
                    window.addEventListener('resize', function() {
                        setTimeout(function() {
                          params.api.sizeColumnsToFit();
                        })
                      })
                }
            };
            
            attr.$observe("columns",function(val){
                debugger;
                var cols =scope.$eval(val);
                if(angular.isUndefined(cols)) {
                    return
                }
                gridOptions.columnDefs =cols;
                $(ele[0]).empty();
                var gEle=$("<div  class=\"ag-theme-fresh\"></div>").appendTo(ele[0]);
                gEle.css({
                    height:$(ele.height())
                })
                cmp =new agGrid.Grid(gEle[0], gridOptions);
                if(attr.id){
                    $parse(attr.id).assign(scope,cmp);
                }


            })
            
        }
    }

}])})(libs_directives || (libs_directives = {}));