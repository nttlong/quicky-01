(function (scope) {
    scope.systemConfig = scope.$root.systemConfig;
	scope.mode = 0;
	scope.showDetail = false;
    scope.filterFunctionModel = '';
	scope.currentFunction = '';
    scope.$display = {
        showDetail: false,
        mapName: [],
        selectedFunction: "",
        selectFunc: function (event, f) {
        scope.$display.selectedFunction = f;
        }
    };

    scope.changeActive = function(event, key){
        $('.hcs-tab-info').find('.active').removeClass('active');
        $('.hcs-tab-info').find('.approver').removeClass('approver');
        $('.hcs-tab-info').find('.waiting_approver').removeClass('waiting_approver');
        $('.hcs-tab-info').find('.deny').removeClass('deny');
        if(key == 1){
            $(event.target).closest('div').addClass('active');
        }
        else if (key==2){
            $(event.target).closest('div').addClass('approver');
        }
        else if (key==3){
            $(event.target).closest('div').addClass('waiting_approver');
        }
        else if (key==4){
            $(event.target).closest('div').addClass('deny');
        }

    }

    scope.tableFields = [
        { "data": "apr_year", "title": "${get_res('apr_year_table_header','Năm')}" },
        { "data": "apr_period", "title": "${get_res('apr_period_table_header','Kỳ đánh giá')}"},
        { "data": "emp_total", "title": "${get_res('emp_total_table_header','Tổng NV')}" , "expr":function(row, data, func){
            func(function(){return "<span class='text-info'>" + data + "<span/>";});
            return true;
        }},
        { "data": "updated", "title": "${get_res('updated_table_header','Đã cập nhật')}", "expr":function(row, data, func){
            func(function(){return "<span class='text-success'>" + data + "<span/>";});
            return true;
        }},
        { "data": "updating", "title": "${get_res('updating_table_header','Đang cập nhật')}", "expr":function(row, data, func){
            func(function(){return "<span class='text-warning'>" + data + "<span/>";});
            return true;
        }},
		{ "data": "not_update", "title": "${get_res('not_update_table_header','Chưa cập nhật')}", "expr":function(row, data, func){
            func(function(){return "<span class='text-danger'>" + data + "<span/>";});
            return true;
        }},
		{ "data": "created_on", "title": "${get_res('create_modified_period','Ngày | Người tạo kỳ')}","expr":function(row, data, func){
            func(function(){
                return window.DateFormat.format(data, scope.systemConfig.date_format) + " | " + " ";
            });
            return true;
        }},
	];
	scope.$$tableConfig = {};
	//Dữ liệu cho table
	scope.tableSource = _loadDataServerSide;
    scope.onSelectTableRow = function ($row) {
        scope.$display.showDetail = scope.$display.showDetail === false ? true : false;
    };

	scope.selectedItems = [];
	scope.currentItem = null;
	scope.tableSearchText = '';
    scope.refreshDataRow = function () { /*Do nothing*/ };
    scope.tableData = _tableData;
    scope.onEdit = onEdit;
    scope.onDelete = onDelete;
	scope.backPage = backPage;
    scope.onSearch = onSearch;

	function backPage() {
        scope.$display.showDetail = scope.$display.showDetail === false ? true : false;
	}

	function handleData() {
		this.collection = {};
        this.mapName = [];
        this.$display = {
            mapName: []
        }

        this.$display.mapName = _.filter(scope.$root.$function_list, function (f) {
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

	function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
		var sort = {};
		$.each(orderBy, function (i, v) {
			sort[v.columns] = (v.type === "desc") ? -1 : -1;
		});
		sort[orderBy[0].columns] =
			services.api("${get_api_key('app_main.api.TMPER_TargetKPI_Emp/get_list_with_searchtext')}")
				.data({
					//parameter at here
					"pageIndex": iPage - 1,
					"pageSize": iPageLength,
					"search": searchText,
					"sort": sort
				})
				.done()
            .then(function (res) {

                _.map(res.items, function(val) {
                    val.emp_total = 0;
                    val.updated = 0;
                    val.updating = 0;
                    val.not_update = 0;

                    return val;
                })


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

    function onSearch(val){

    }

    function onEdit(){
        if(scope.currentItem)
            scope.$display.showDetail = true;
        else
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_res('no_apr_period_selected','Chưa chọn kỳ đánh giá')}", function () { });
    }

    function onDelete() {
        scope.mode = 3;
        if (!scope.selectedItems || scope.selectedItems.length === 0) {
            $msg.message("${get_global_res('Notification','Thông báo')}", "${get_global_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
        } else {
            $msg.confirm("${get_global_res('Notification','Thông báo')}", "${get_global_res('Do_You_Want_Delete','Bạn có muốn xóa không?')}", function () {
                services.api("${get_api_key('app_main.api.TMPER_TargetKPI_Emp/delete')}")
                    .data(scope.selectedItems)
                    .done()
                    .then(function (res) {

                        if (res.deleted > 0) {
                            _tableData(scope.$$tableConfig.iPage, scope.$$tableConfig.iPageLength, scope.$$tableConfig.orderBy, scope.$$tableConfig.SearchText, scope.$$tableConfig.fnReloadData);
                            $msg.alert("${get_global_res('Handle_Success','Thao tác thành công')}", $type_alert.INFO);
                            scope.$applyAsync();
                            scope.currentItem = null;
                            scope.selectedItems = [];
                        }
                    })
            });
        }
    };

	(function _init_() {
        scope.handleData = new handleData();
        scope.$display.mapName = scope.handleData.$display.mapName;
        scope.currentFunction = scope.$display.mapName[0];
        scope.$root.$$$authoriseFunction.id = scope.$root.currentFunction.function_id;
        scope.$display.selectedFunction = (scope.$display.mapName.length > 0) ? scope.$display.mapName[0].function_id : null;
		scope.$applyAsync();
	})();

    scope.$root.$history.onChange(scope, function (data) {
        if(!_.findWhere(scope.$root.$function_list, {function_id:data['page']}))
        {
            data = {
                page: data.hasOwnProperty('page') ? scope.$root.$extension.TripleDES.decrypt(data.page) : null,
                f: data.hasOwnProperty('f') ? scope.$root.$extension.TripleDES.decrypt(data.f) : null,
            }
        }else{
            window.location.href = '#page=' + scope.$root.$extension.TripleDES.encrypt(data['page']);
        }
    });

});