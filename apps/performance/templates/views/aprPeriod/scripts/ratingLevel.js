(function (scope) {
    debugger
    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields": [
            { "data": "department_code", "title": "${get_res('department_code','Mã')}", width: "100px", className: "text-left" }
        ],
        "selectTreeNode": function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false,

    };

    scope.addDataGeneration = addDataGeneration
    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;
    scope.onExport = onExport;
    scope.onImport = onImport;

    

    function addDataGeneration() {
        scope.mode = 4;// set mode tạo mới
        openDialog("${get_res('generate_data','Phát sinh Định mức xếp loại')}", 'aprPeriod/form/genRatingLevel', function () { });
    };

   
    //function _init_() {
    //    var a = Re_Map_Period(scope.$parent.currentItem.apr_period);
    //    var b = scope.$parent.currentItem.apr_year;
    //    _departmentGroup(a, b);
    //}

    (function _departmentGroup() {
        debugger
        var arrTableTree = {};
        services.api("${get_api_key('app_main.api.TMPER_AprPeriodRank/get_tree')}")
            .data({
                apr_period: Re_Map_Period(scope.$parent.entity.apr_period),
                apr_year: scope.$parent.entity.apr_year
            })
            .done()
            .then(function (res) {
                debugger
                if (res.length > 0) {
                    res.push({
                        level: 1,
                        parent_code: null,
                        department_code: "LV",
                        department_name: "Công ty Cổ phần Tin học Lạc Việt",
                        level_code: ["LV"],
                        ordinal: "DP001"
                    })
                }


                res_rankField = _.map(res, function (val, index) {
                    Object.assign(res[index], { rank3: 40 });
                    return { "data": val.rank_code, "title": "%" + "<" + val.rank_name + ">", width: "50px", className: "text-center" };

                })
                for (var i = 0; i < res_rankField.length - 1; i++) {
                    scope.$$tableTree.tableFields.push(res_rankField[i]);

                }
                debugger
                scope.$$tableTree.tableFields;
                console.log("@@@@@:", scope.$$tableTree.tableFields)
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();

            })
    })();

    
    
    //(function getListRankCode() {
    //    debugger
    //    services.api("${get_api_key('app_main.api.TMLS_Rank/getListRankcode')}")
    //        .data()
    //        .done()
    //        .then(function (res) {
    //            debugger
    //            res = _.map(res, function (val) {
    //                return { "data": val.rank_code, "title": "%"+ "<"+ val.rank_name +">", width: "100px", className: "text-center"  };
    //            })
    //            for (var i=0; i < res.length; i++) {
    //                scope.$$tableTree.tableFields.push(res[i]);
    //            }
    //            scope.$applyAsync();
    //        });
    //})();
    
   
    function onAdd() {
        scope.mode = 1;
        openDialog("${get_res('Rating_Level_Detail','Chi tiết định mức xếp loại')}", 'aprPeriod/form/addRatingLevel', function () { });
    };


    function onDelete() {
        if (!scope.$$tableTree.treeSelectedNodes[0]) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else {
            scope.mode = 3;
            //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMPER_AprPeriodRank/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                            scope.$applyAsync();
                            scope.a = _departmentGroup;
                        }
                        else
                            $msg.alert("${get_global_res('Handle_Fail','request paramerter is not exist')}", $type_alert.INFO);
                    });
            });
        }
    }

    function onEdit() {
        scope.mode = 2;
        openDialog("${get_res('Employee_Not_Approval_Detail','Chi tiết Nhân viên không đánh giá')}", 'aprPeriod/form/addRatingLevel', function () { });
    };

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
    function Re_Map_Period(periodStr) {
        debugger
        var numPeriod = 0;
        for (var i = 0; i < 12; i++) {
            if (periodStr === "Tháng " + (i + 1).toString()) {
                numPeriod = i + 1
                return numPeriod;
            }

        }
        for (var j = 13; j <= 16; j++) {
            if (periodStr === "Quý " + (j - 12).toString()) {
                numPeriod = j - 12
                return numPeriod;
            }
        }
        if (periodStr === "6 tháng đầu năm")
            numPeriod = 17;
        else if (periodStr === "6 tháng cuối năm")
            numPeriod = 18;
        else
            numPeriod = 19;
        return numPeriod;
    }
    

    
    
});