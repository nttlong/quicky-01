(function (scope) {
    //Cấu hình tên field và caption hiển thị trên UI
    scope.tableFields = [
        { "data": "room_code", "title": "${get_res('room_code','Mã Phòng')}" },
        { "data": "room_name", "title": "${get_res('room_name','Tên Phòng')}" },
        { "data": "room_name2", "title": "${get_res('room_name2','Tên Phòng Khác')}" },
        { "data": "supplier_code", "title": "${get_res('supplier_code','Trung Tâm')}" },
        { "data": "room_map", "title": "${get_res('room_map','Sơ đồ Phòng')}" },
        { "data": "note", "title": "${get_res('note','Note')}" },
        { "data": "ordinal", "title": "${get_res('ordinal','Thứ tự')}" },
        { "data": "lock", "title": "${get_res('lock','Ngưng SD')}", "format": "checkbox"}
    ];
    scope.onSelectTableRow = pressEnter;
    scope.tableSource = _loadDataServerSide;
    scope._tableData = _tableData;

    scope.onSearch = onSearch;
    function pressEnter($row) {
        scope.editRoom();
    }

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$tableConfig = {
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

    //
    scope.tableSearchText = '';
    scope.SearchText = '';

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "desc") ? -1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("${get_api_key('app_main.api.HCSLS_Room/get_list_with_searchtext')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort
                })
                .done()
                .then(function (res) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.currentItem = null;
                    scope.$apply();
                })
    }

    // Insert 
    scope.addRoom = function(){
    };
    /**
    * Hàm mở form chỉnh sửa
    */
    scope.editRoom = function () {
    }
    /**
    * Hàm mở form delete
    */
    scope.delRoom = function () {
    }
    function onSearch(val) {
        scope.tableSearchText = val;
        scope.$apply();
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
        if ($('#myModal').length === 0) {
            scope.headerTitle = title;
            //Đặt ID cho form dialog
            dialog(scope, id).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
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

    function init() {
        scope.handleData = new handleData();
        scope.mapName = scope.handleData.mapName;
        scope.currentFunction = scope.mapName[0];
    }

    init();

    scope.$watch("selectedFunction", function (function_id) {
        if (function_id) {
            var $his = scope.$root.$history.data();
            window.location.href = "#page=" + $his.page + "&f=" + function_id;
        }
    });

    scope.$root.$history.onChange(scope, function (data) {
        if (scope.mapName.length > 0) {
            if (data.f) {
                var func = _.filter(scope.mapName, function (f) {
                    return f["function_id"] == data.f;
                });
                if (func.length > 0) {
                    scope.$partialpage = func[0].url;
                    scope.currentFunction = func[0];
                    scope.selectedFunction = func[0].function_id;
                } else {
                    window.location.href = "#";
                }
            } else {
                scope.$partialpage = scope.mapName[0].url;
            }
            scope.$apply();
        } else {
            window.location.href = "#";
        }
    });
});