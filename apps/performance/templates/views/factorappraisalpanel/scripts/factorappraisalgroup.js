﻿(function (scope) {
    scope.$parent.$parent.$parent.isChangeFunc = false;
    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields" : [
            { "data": "factor_group_code", "title": "${get_res('function_list','Mã nhóm')}", width: "100px", className: "text-center"},
            { "data": "note", "title": "${get_res('note','Ghi chú')}", width: "100px", className: "text-center"},
            { "data": "ordinal", "format":"number: system", "title": "${get_res('ordinal','Thứ tự')}", width: "100px", className: "text-center"},
            { "data": "lock", "title": "${get_res('lock','Ngưng sử dụng')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        "selectTreeNode" : function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treePressEnter":onEdit,
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false,
        
    };

    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;
    scope.onExport = onExport;
    scope.onImport = onImport;

   
    //page load first 
    scope.$$tableTree.dataTableTree = [];
    scope._reloadpage = _factorAppraisalGroup;
    //enter-press in row
   
    // reload data
    function _factorAppraisalGroup() {
        services.api("${get_api_key('app_main.api.TMLS_FactorAppraisalGroup/get_tree')}")
            .data()
            .done()
            .then(function (res) {
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();
            })
    }

    

    function onAdd() {
            scope.mode = 1;
            openDialog("${get_res('Factor_Appraisal_Group_Detail','Chi tiết nhóm yếu tố đánh giá')}", 'factorappraisalpanel/form/addFactorAppraisalGroup', function () { });
    };


    function onDelete() {
        if (!scope.$$tableTree.treeSelectedNodes[0]) {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
        else
        {
            scope.mode = 3;
            //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_FactorAppraisalGroup/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
						if (res.deleted > 0) {
							scope._reloadpage();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                        }
                        else if (res['error'] == "not allow") {
                            $msg.message("${get_global_res('Notification_not_allow','Không được phép')}", "${get_global_res('Row_Selected_using_by_other_factor','Dòng được chọn đang được sử dụng bởi yếu tố')}", function () { });
                        }
                        else
                            $msg.alert("${get_global_res('Handle_Fail','request paramerter is not exist')}", $type_alert.INFO);
                    });
            });
        }
    }

    function onEdit() {
            scope.mode = 2; 
            openDialog("${get_res('Factor_Appraisal_Group_Detail','Chi tiết nhóm yếu tố đánh giá')}", 'factorappraisalpanel/form/addFactorAppraisalGroup', function () { });
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

    _factorAppraisalGroup();
});