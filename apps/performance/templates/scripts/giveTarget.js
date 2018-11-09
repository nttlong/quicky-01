﻿(function (scope) {
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
        { "data": "apr_year", "title": "${get_res('apr_year_table_header','Năm')}", "className": "text-center" },
        { "data": "apr_period.caption", "title": "${get_res('apr_period_table_header','Kỳ đánh giá')}", "className": "text-left"},
        { "data": "not_rate", "title": "${get_res('not_rate','Không ĐG')}", "className": "text-center"},
        { "data": "total_give", "title": "${get_res('total_give','Tổng ĐG')}", "className": "text-center" },
        { "data": "gived.on_time", "title": "${get_res('give_on_time','Giao đúng hạn')}", "className": "text-center" },
		{ "data": "gived.over", "title": "${get_res('give_over','Giao trễ hạn')}", "className": "text-center" },
        { "data": "not_rate", "title": "${get_res('not_give','Chưa giao')}", "className": "text-center" },
        { "data": "status_assign", "title": "${get_res('status','Trạng thái')}", "className": "text-center", "expr": function(row, column, func){
            func(function(){
                return column == 0 ? '<span class="hcs-square-icon grey"></span>' : column == 1 ? '<span class="hcs-square-icon cyan"></span>' + "${get_res('on_time','Đúng hạn')}" : '<span class="hcs-square-icon orange"></span>' + "${get_res('delay','Trễ hạn')}";
            });
            return true;
        } },
        { "data": "created_by", "title": "${get_res('created_on_and_created_by','Ngày tạo| Người tạo kỳ')}", "expr": function(row, colmn, func){
            func(function(){
                return scope.$root.$formatSystem.date(row['created_on']) + " | " + row['created_by'];
            });
            return true;
        }}
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
			services.api("${get_api_key('app_main.api.TMPER_AprPeriod/get_give_target_list_main')}")
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