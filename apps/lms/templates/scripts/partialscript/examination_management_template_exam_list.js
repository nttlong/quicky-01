(function (scope) {
    scope.$parent.$partialpage = "partialpage/examination_management_template_exam_list";

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        //if ($('#myModal').length === 0) {
        scope.headerTitle = title;
        //Đặt ID cho form dialog
        dialog(scope, id).url(path).done(function () {
            callback();
            //Set draggable cho form dialog
            $dialog.draggable();
        });
        //}
    }

    scope.$root.createTemplate = function () {
        
        scope.mode = 1; // set mode chỉnh sửa
        openDialog("${get_res('Create_exam_category','Create Exam Category')}", 'form/addTemplateCategory', function () {
            setTimeout(function () {
                $(window).trigger('resize');
            }, 200);
        });
    }

    scope.$root.editTemplate = function () {
        
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('edit_exam_category','Edit Exam Category')}", 'form/addTemplateCategory', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });

        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.$root.delTemplate = function () {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el && el._id
        })
        //
        if (scope.selectedItems.length > 0) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_ExTemplateCategory/delete')}")
                    .data(arrayId)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.currentItem = [];
                            scope.$root.refresh();
                        }
                    })
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.$root.isDisplay = true;
    scope.__tableSource = [];
    scope.mode = 0;
    scope.showDetail = false;
    scope.filterFunctionModel = ''
    scope.currentFunction = '';
    scope.mapName = [];
    scope.$parent.isDisplayGird = true;
    scope.$root.onDisplayListData = function () {
        scope.selectedItems = []
    }
    scope.$root.onDisplayGridData = function () {
        scope.selectedItems = []
    }
    scope.objSearch = {
        $$$modelSearch: null,
        onSearch: onSearch
    }
    /* Table */
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "exam_temp_id", "title": "${get_res('exam_temp_id_table_header','ID')}" },
        { "data": "exam_temp_category", "title": "${get_res('exam_temp_category_table_header','Exam Category')}" },
        { "data": "exam_temp_name1", "title": "${get_res('exam_temp_name1_header','Exam Template')}" },
        { "data": "total_question", "title": "${get_res('total_question_table_header','Questions')}" },
        { "data": "total_mask", "title": "${get_res('total_mask_table_header','Total Marks')}" },
        { "data": "negative_marks", "title": "${get_res('negative_marks_table_header','Required Score')}" },
        { "data": "diff_question", "title": "${get_res('diff_question_header','Difficult Questions')}" },
        { "data": "med_question", "title": "${get_res('med_question_header','Medium Questions')}" },
        { "data": "easy_question", "title": "${get_res('easy_question_table_header','Easy Questions')}" },
        { "data": "creator", "title": "${get_res('created_by_table_header','Created by')}" },
        { "data": "created_on", "title": "${get_res('created_on_table_header','Created on')}", "format": "date:" + 'dd/MM/yyyy h:mm:ss a'  },
    ];
    scope.$$tableConfig = {};
    scope.$root.$$tableConfig = {};
    scope.$root._tableData = _tableData;
    scope.$root._departments = _departments;
    //Dữ liệu cho table
    scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.mode = 2;
        scope.$root.edit();
    };
    //Danh sách các dòng đc chọn (nếu là table MultiSelect)
    scope.selectedItems = [];
    //Dòng hiện tại đang được focus (nếu table là SingleSelect hoặc MultiSelect)
    scope.currentItem = null;
    scope.tableSearchText = '';
    scope.SearchText = '';
    //Refesh table
    scope.refreshDataRow = refresh;
    scope.$root.refresh = refresh;

    /* Tree */
    scope.treeCurrentNode = {};
    scope.treeSelectedNodes = [];
    scope.treeSelectedRootNodes = [];
    scope.treeCheckAll = false;
    scope.treeSearchText = '';
    scope.treeDisable = false;
    scope.treeMultiSelect = false;
    scope.treeMode = 3; // Value in (1, 3) combobox toàn quyền set 1 ngược lại set 3
    var _treeDepartmentsDataSource = null;
    scope.treeDepartmentsDataSource = null;

    //selectbox datasource
    scope.cbbGender = [];
    scope.cbbEmployeeActive = [];
    scope.cbbCulture = [];
    scope.cbbRetrain = [];
    scope.cbbTrainLevel = [];
    scope.cbbLabourType = [];
    scope.cbbLevelManagement = [];
    scope.cbbWorkingType = [];

    //navigation button
    scope.firstRow = firstRow;
    scope.previousRow = previousRow;
    scope.nextRow = nextRow;
    scope.lastRow = lastRow;

    //function button
    scope.addEmployee = addEmployee;
    scope.refresh = refresh;

    //Navigation: quay trở về UI list
    scope.backPage = backPage;
    scope.$root.createTemplate = function () {
        scope.mode = 1; // set mode chỉnh sửa
        openDialog("${get_res('Create_an_exam_template','Create an Exam Template')}", 'form/addExamTemplate', function () {
            setTimeout(function () {
                $(window).trigger('resize');
            }, 200);
        });
    }

    scope.$root.editTemplate = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('edit_an_exam_template','Edit an Exam Template')}", 'form/addExamTemplate', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });

        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.$root.delTemplate = function () {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el && el._id
        })
        //
        if (scope.selectedItems.length > 0) {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.LMSLS_ExTemplateCategory/delete')}")
                    .data(arrayId)
                    .done()
                    .then(function (res) {
                        if (res.deleted > 0) {
                            scope.currentItem = [];
                            scope.$root.refresh();
                        }
                    })
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    function backPage() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 0;
            $(window).trigger('resize');
        }, 500);
    }

    function addEmployee() {
        $('.hcs-profile-list').fadeToggle();
        setTimeout(function () {
            scope.showDetail = scope.showDetail === false ? true : false;
            scope.mode = 1;
            scope.currentItem = {};
            scope.$partialpage = scope.mapName[0].url;
            $(window).trigger('resize');
        }, 500);
    }

    function refresh() {
        var tableConfig = scope.$$tableConfig;
        _tableData(tableConfig.iPage,
            tableConfig.iPageLength, tableConfig.orderBy,
            tableConfig.searchText, tableConfig.fnReloadData);
        _departments();
    }

    function firstRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[0];
        }
    }

    function previousRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === 0 ? scope.__tableSource.length - 1 : idx_item - 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function nextRow() {
        if (scope.__tableSource.length > 0) {
            var idx_item = _.findIndex(scope.__tableSource, { "employee_code": scope.currentItem.employee_code });
            var index = idx_item === (scope.__tableSource.length - 1) ? 0 : idx_item + 1;
            scope.currentItem = scope.__tableSource[index];
        }
    }

    function lastRow() {
        if (scope.__tableSource.length > 0) {
            scope.currentItem = scope.__tableSource[scope.__tableSource.length - 1];
        }
    }



    function handleData() {

        this.collection = {};

        this.mapName = [];

        this.mapName = _.filter(scope.$root.$function_list, function (f) {
            return f.level_code.includes(scope.$root.currentFunction.function_id)
                && f.level_code.length == scope.$root.currentFunction.level_code.length + 1
        });

        this.getElementMapNameByIndex = (index) => {
            return mapName[index];
        }
    };

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText

        };
        scope.$root.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
        //setTimeout(function () {
        if (fnReloadData) {
            if (searchText) {
                _tableData(iPage, iPageLength, orderBy, searchText, function (data) {
                    fnReloadData(data);
                });
            } else {
                _tableData(iPage, iPageLength, orderBy, null, function (data) {
                    fnReloadData(data);
                });
            }
        }
        //}, 1000);
    };

    scope._tableData = _tableData;
    function _tableData(iPage, iPageLength, orderBy, searchText, callback, objSearchAdvance) {
        
        //if (scope.treeCurrentNode.hasOwnProperty('folder_id')) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.LMSLS_ExTemplateList/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "where": {

                    },
                    "sort": sort,
                })
                .done()
            .then(function (res) {
                    
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    scope.ItemTables = JSON.parse(JSON.stringify(data.data));
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
        //}
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog\
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
        //check tồn tại của form dialog theo id
        //if ($('#myModal').length === 0) {
        scope.headerTitle = title;
        //Đặt ID cho form dialog
        dialog(scope, id).url(path).done(function () {
            callback();
            //Set draggable cho form dialog
            $dialog.draggable();
        });
        //}
    }

    function _departments() {
        services.api("${get_api_key('app_main.api.LMSLS_ExTemplateCategory/get_list')}")
            .data()
            .done()
            .then(function (res) {
                _treeDepartmentsDataSource = res;
                scope.treeDepartmentsDataSource = _treeDepartmentsDataSource;
                scope.treeCurrentNode = res[0];
                scope.$applyAsync();
            })
    }

    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$applyAsync();
    }

    function _selectBoxData() {
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": [
                    "LGender",
                    "LEmployeeActive",
                    "LCulture",
                    "LRetrain",
                    "LTrainLevel",
                    "LLevelManagement",
                    "LWorkingType",
                    "LLabourType"
                ]
            })
            .done()
            .then(function (res) {
                scope.cbbGender = getValue(res.values, "LGender");
                scope.cbbEmployeeActive = getValue(res.values, "LEmployeeActive");
                scope.cbbCulture = getValue(res.values, "LCulture");
                scope.cbbRetrain = getValue(res.values, "LRetrain");
                scope.cbbTrainLevel = getValue(res.values, "LTrainLevel");
                scope.cbbLabourType = getValue(res.values, "LLabourType");
                scope.cbbLevelManagement = getValue(res.values, "LLevelManagement");
                scope.cbbWorkingType = getValue(res.values, "LWorkingType");
                scope.$applyAsync();
                function getValue(response, listName) {
                    return _.findWhere(response, { "list_name": listName }) ? _.findWhere(response, { "list_name": listName }).values : [];
                }
            })
    }

    (function _init_() {
        _departments();
        _selectBoxData();
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
        scope.selectedFunction = (scope.mapName.length > 0) ? scope.mapName[0].function_id : null;
        scope.$applyAsync();
    })();

    scope.$watch("selectedFunction", function (function_id) {
        console.log(function_id);
        var $his = scope.$root.$history.data();
        if (scope.currentItem)
            window.location.href = "#page=" + $his.page + "&f=" + function_id;
    });

    scope.$watch("$parent.searchText", function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, val)
        /*
        scope.SearchText =val*/
        scope.$applyAsync();
    });
    /* scope.$watch("objSearch.onSearch", function () {
         
         scope.$root.currentItem.push(scope.currentItem);
         scope.$applyAsync();
     });*/

    //scope.$root.$history.onChange(scope, function (data) {
    //    if (scope.mapName.length > 0) {
    //        if (data.f) {
    //            scope.$partialpage = _.filter(scope.$root.$functions, function (f) {
    //                return f.function_id = data.f
    //            })[0].url;
    //            var func = _.filter(scope.mapName, function (f) {
    //                return f["function_id"] == data.f;
    //            });
    //            if (func.length > 0) {
    //                scope.$partialpage = func[0].url;
    //                scope.currentFunction = func[0];
    //            } else {
    //                window.location.href = "#";
    //            }
    //        } else {
    //            //scope.$partialpage = scope.mapName[0].url;
    //        }
    //        scope.$apply();
    //    } else {
    //        window.location.href = "#";
    //    }
    //});

    scope.$watch('treeCurrentNode', function (val) {
        _loadDataServerSide(scope.$$tableConfig.fnReloadData,
            1, scope.$$tableConfig.iPageLength,
            scope.$$tableConfig.orderBy, scope.$$tableConfig.searchText)
    })

    scope.$root.viewDetailsLearningMaterial = function () {

        if (scope.currentItem) {
            services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/update_view_file')}")
                .data({
                    "where": {
                        'id': scope.currentItem['_id'],
                        'views': 1,
                    }
                })
                .done()
                .then(function (res) {
                })

            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_LearningMaterial','Create New Folder')}", 'form/viewDetailsLearningMaterialManagement', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }
    scope.$root.viewShareFileLearningMaterial = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('Detail_LearningMaterial','Create New Folder')}", 'form/viewShareFileLearningMaterial', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }

    }


    scope.$root.viewHistoryLearningMaterial = function () {
        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('History_LearningMaterial','Xem lịch sử')}", 'form/viewHistoryLearningMaterialManagement', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.$root.viewPermisitonLearningMaterial = function () {

        if (scope.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('History_LearningMaterial','Xem lịch sử')}", 'form/permissionsLearningMaterialManagement', function () {
                setTimeout(function () {
                    $(window).trigger('resize');
                }, 200);
            });
        } else {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        }
    }

    scope.fnSelectDataGrid = fnSelectDataGrid;

    function fnSelectDataGrid(item) {
        scope.currentItem = item ? item : scope.currentItem;
        scope.$applyAsync();
    }

    scope.onCheckItemGird = function (item) {
        var arrayId = scope.selectedItems.filter(function (el) {
            return el._id == item._id
        })
        if (arrayId.length > 0) {
            var arrayItem = scope.selectedItems.filter(function (el) {
                return el._id != item._id
            })
            scope.selectedItems = arrayItem;
        } else {
            scope.selectedItems.push(item);
        }

    }

    scope.getNumber = function (num) {
        var arr = [];
        for (var i = 0; i < num; i++) {
            arr.push(i);
        };
        return arr;
    }


    scope.getStars = function (rating) {
        // Get the value
        var val = parseFloat(rating);
        // Turn value into number/100
        var size = val / 5 * 100;
        return size + '%';
    }

    scope.convertFileSize = function (size) {
        if (size < 1024) {
            return size.toFixed(2) + " B";
        } else if (size < 1024 * 1024) {
            return (size / 1024).toFixed(2) + " KB";
        } else if (size < 1024 * 1024 * 1024) {
            return (size / (1024 * 1024)).toFixed(2) + " MB";
        } else if (size < 1024 * 1024 * 1024 * 1024) {
            return (size / (1024 * 1024 * 1024)).toFixed(2) + " TB";
        } else {
            return (size / (1024 * 1024 * 1024 * 1024)).toFixed(2) + " GB";
        }
    }

});