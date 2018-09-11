(function (scope) {
    scope.$$tableTree = {
        "dataTableTree": [],
        "tableFields": [
            { "data": "com_group_code", "title": "${get_res('com_group_code','Mã nhóm')}", width: "100px", className: "text-center" },
            { "data": "ordinal", "title": "${get_res('ordinal','Thứ tự')}", width: "100px", className: "text-center" },
            { "data": "lock", "title": "${get_res('lock','Ngưng sử dụng')}", format: "checkbox", width: "100px", className: "text-center" }
        ],
        "selectTreeNode": function (node) {

        },
        "treeCurrentNode": {},
        "treeSelectedNodes": [],
        "treeSelectedRootNodes": [],
        "treeMultiSelect": true,
        "treeSelectMode": 3,
        "treeDisabled": false,
        "lock": 0
    };

    scope.$parent.$parent.$parent.onAdd = onAdd;
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onImport = onImport;
    scope.$parent.$parent.$parent.onExport = onExport;
    //scope.$parent.$parent.$parent.onAttach = onAttach;
    scope.$parent.$parent.$parent.onRefresh = onRefresh;
    scope.$parent.$parent.$parent.onPrint = onPrint;

    scope._competencyGroup = _competencyGroup;

    function _competencyGroup() {
        services.api("${get_api_key('app_main.api.TMLS_CompetencyGroup/get_tree')}")
            .data({
                lock: scope.$parent.$parent.$parent.advancedSearch.data_lock,
            })
            .done()
            .then(function (res) {
                scope.$$tableTree.dataTableTree = res;
                scope.$applyAsync();
            })
    }

    function onPrint() {

    }

    function onRefresh() {
        _competencyGroup();
    }

    /**
     * Hàm mở form tạo moi
     */
    function onAdd() {
        scope.mode = 1;// set mode tạo mới
        openDialog("${get_res('Detail_Competency_Group','Chi tiết nhóm năng lực')}", 'competencyDictionary/form/addCompetencyGroup', function () { });
    }
    function onEdit() {
        scope.mode = 2;
        openDialog("${get_res('Detail_Competency_Group','Chi tiết nhóm năng lực')}", 'competencyDictionary/form/addCompetencyGroup', function () { });
    };

    function onDelete() {
        if (!scope.$$tableTree.treeSelectedNodes[0]) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
        else {
            scope.mode = 3;
            //Kiểm tra node có được dùng ở tag yếu tố đánh giá hay không.(nếu có thì delete not allow)
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMLS_CompetencyGroup/delete')}")
                    .data(scope.$$tableTree.treeSelectedNodes)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            _competencyGroup();
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.SUCCESS);
                        }
                        else if (res['error'] == "CompetencyGroup is using another PG") {
                            $msg.alert("${get_global_res('node_selected_use_other_process','Nút được chọn đang được sử dụng bởi xử lí khác')}", $type_alert.INFO);
                        }
                        else {
                            $msg.alert("${get_global_res('Handle_failed','Thao tác thất bại')}", $type_alert.DANGER);
                        }
                    });
            });
        }
    }
    function onImport() {

    };
    function onExport() {

    };
    function onAttach() {

    };

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    (function __init__() {
        _competencyGroup();
    })();

    scope.$parent.$watch("advancedSearch.data_lock", function (old, newVal) {
        if (old != newVal)
            _competencyGroup();
    });
});