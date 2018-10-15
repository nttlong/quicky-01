(function (scope) {
    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields": [
            { "data": "department_code", "title": "${get_res('department_code','Mã')}", width: "auto", className: "text-left" }
        ],
        "selectTreeNode": function (node) {

        },
        "treeCurrentNode": {},
        "treePressEnter": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false,
        "formatMainColumn": {},
    };


    scope.$parent.$parent.$parent.onGen = addDataGeneration
     //var a = scope.$parent.currentFunction.function_id ;
    scope.$parent.$parent.$parent.onAdd =  onAdd;
    scope.$parent.$parent.$parent.onSearch = onSearch;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete =  onDelete;
    scope.$parent.$parent.$parent.onImport =  onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach =  onAttach;
    scope.$parent.$parent.$parent.onRefresh =  onRefresh;
    scope.onExport = onExport;
    scope.onImport = onImport;

    scope.$$tableTree.formatMainColumn = function(format,row,columns){
        format(function(){
            return "<span style='font-weight:bold'>" + columns + "</span>";
            })
         return row.rank_level && row.rank_level.length>0;
    }

    scope.$$tableTree.treePressEnter = function(data){
        onEdit();
    }

    function addDataGeneration() {
        scope.mode = 4;// set mode tạo mới
        openDialog("${get_res('generate_data','Phát sinh Định mức xếp loại')}", 'aprPeriod/form/genRatingLevel', function () { });
    };
    scope._departmentGroup = _departmentGroup();
    function _departmentGroup() {
    debugger
        services.api("${get_api_key('app_main.api.TMPER_AprPeriodRank/get_tree')}")
            .data({
                apr_period: scope.$parent.mode == 1 ? scope.$parent.apr_period_now : scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period),
                apr_year: scope.$parent.mode == 1 ? scope.$parent.apr_year_now : scope.$parent.entity.apr_year
            })
            .done()
            .then(function (res) {
                if (res.length <= 0) {
                    res = null;
                }
                else {
                services.api("${get_api_key('app_main.api.HCSSYS_Departments/getRootDepartment')}")
                .data(res)
                .done()
                .then(function(res1){
                    res1.forEach(function(el){
                        el._id = null;
                        el.apr_period = scope.$parent.mode == 1 ? scope.$parent.apr_period_now : scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period),
                        el.apr_year = scope.$parent.mode == 1 ? scope.$parent.apr_year_now : scope.$parent.entity.apr_year
                        debugger
                        for (var i=0; i<res.length; i++){
                            if(res[i].level_code.includes(el.department_code)){
                                res.push(el);
                                break;
                            }
                        }
                    });
                });
                }
                debugger
                   scope.$$tableTree.tableFields = scope.$$tableTree.tableFields.concat(scope.$parent.$$$tableFields);
                   scope.$$tableTree.dataTableTree = res;
                    scope.$applyAsync();

                });
    }



    (function getListRankCode(callback) {
        services.api("${get_api_key('app_main.api.TMLS_Rank/getListRank')}")
            .data()
            .done()
            .then(function (res) {
                scope.$rating = res;
                res = _.map(res, function (val) {
                    return { "data": val.rank_code, "title": "%"+ "<"+ val.rank_name +">", width: "100px", className: "text-left" };
                })
                scope.$parent.$$$tableFields = res;
                callback(res)
                scope.$applyAsync();
            });
        })();


    function onAdd() {
        scope.mode = 1;
        openDialog("${get_res('Rating_Level_Detail','Chi tiết định mức xếp loại')}", 'aprPeriod/form/addRatingLevel', function () { });
    }

    function onDelete() {
    debugger
        if (!scope.$$tableTree.treeSelectedNodes || scope.$$tableTree.treeSelectedNodes.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                scope.$$tableTree.treeSelectedRootNodes.forEach(function(el){
                if(el.apr_period == undefined){
                    el.apr_period = scope.$parent.mode == 1 ? scope.$parent.apr_period_now : scope.$parent.Re_Map_Period(scope.$parent.entity.apr_period);
                   el.apr_year = scope.$parent.mode == 1 ? scope.$parent.apr_year_now : scope.$parent.entity.apr_year;
                }
                });
                services.api("${get_api_key('app_main.api.TMPER_AprPeriodRank/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                             _departmentGroup();
                        }
                    })
            });
        }
    };

    function onEdit() {
        scope.mode = 2;
        debugger
         if (!scope.$$tableTree.treeSelectedNodes || scope.$$tableTree.treeSelectedNodes.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else if(!scope.$$tableTree.treeCurrentNode || scope.$$tableTree.treeCurrentNode.rank_level == null ){
        $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('Department_Selected_Not_Data','Phòng ban được chọn không chứa dữ liệu')}", function () { });
        }
        else{
        openDialog("${get_res('level_rank_Detail','Chi tiết Định mức Xếp loại')}", 'aprPeriod/form/addRatingLevel', function () { });
        }

    };

    function onSearch(val) {
        scope.$$tableTree.treeSearchText = val;//scope.SearchText;
        scope.$apply();
    }

    function onImport() {
        lv.ImportFile("${get_api_key('app_main.excel.import/call')}")
            .done(function (res) {
                console.log("lv.UploadService", res);
            });
    };
    function onExport() {
        lv.ExportFile("/excel_export")
            .data({
                'collection_name': 'HCSLS_EmployeeType'
            }).done();
    }

    function onAttach() {

    };
    function onRefresh() {

    };
    scope.$watch('$$tableTree.treeSelectedNodes', function (val) {
        console.log("myTreeSelected"+val);
    });
    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {

        //check tồn tại của form dialog theo id
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }


    }

    

    
    
});