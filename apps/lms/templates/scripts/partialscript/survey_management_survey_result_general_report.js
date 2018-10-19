(function (scope) {
    scope.$$display = {
        detail: true
    }
    scope.$$table = {
        tableFields: [
            { "data": "category_id", "title": "${get_res('id','ID')}", "className": "text-left" },
            { "data": "category_name", "title": "${get_res('question_category_name','Tên')}", "className": "text-left" },
            { "data": "question_group_display", "title": "${get_res('question_group','Nhóm câu hỏi')}", "className": "text-left" },
            { "data": "num_of_questions", "title": "${get_res('number_of_questions','Số câu hỏi')}", "className": "text-center" },
            { "data": "created_on", "title": "${get_global_res('created_on','Ngày tạo')}", "format": "date:" + scope.$root.systemConfig.date_format, "className": "text-center" },
            { "data": "ordinal", "width":"50px", "title": "${get_global_res('ordinal','Thứ tự')}", "className": "text-center" },
            { "data": "active", "width":"50px", "title": "${get_res('disabled','Ngưng sử dụng')}", "format": "checkbox", "className": "text-center" }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { scope.onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };

    function _loadDataServerSide(fnReloadData, iPage, iPageLength, orderBy, searchText) {
        scope.$$table.$$tableConfig = {
            fnReloadData: fnReloadData,
            iPage: iPage,
            iPageLength: iPageLength,
            orderBy: orderBy,
            searchText: searchText
        };
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
    };

    function _tableData(iPage, iPageLength, orderBy, searchText, callback) {
        var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
        services.api("${get_api_key('app_main.api.LMS_SurQuestionCategoryController/get_list')}")
            .data({
                //parameter at here
                "pageIndex": iPage - 1,
                "pageSize": iPageLength,
                "search": searchText,
                "sort": sort
            })
            .done()
            .then(function (res) {
                if (res.items) {
                    var data = {
                        recordsTotal: res.total_items,
                        recordsFiltered: res.total_items,
                        data: res.items
                    };
                    callback(data);
                    scope.$$table.currentItem = null;
                    scope.$apply();
                }
            })
    }


    scope.$root.extendToolbar = false;
    scope.dashBoard = {}
    scope.labelSetChart = [];
    (function getLabelDateChart() {
        var arr = [];
        for (var i = 0; i < 10; i++) {
            arr.push(moment().subtract(i, 'd').format('DD/MM/YYYY'));
        }
        scope.labelSetChart = arr.reverse();
    })();

    scope.$chartLine = {
        numberView: 10,

    };
    scope.dataSetChart = '';
    scope.labelSetChart = scope.labelSetChart;
    scope.labelsPie = [];
    scope.dataPie = [];
    scope.colorsPie = ['#803690', '#00ADF9', '#DCDCDC', '#46BFBD', '#FDB45C']

    scope.arrData = function (list) {


    }
    scope.labelsHorizontalBar = [];

    //scope.seriesHorizontalBar = ['Series A', 'Series B'];

    scope.dataHorizontalBar = [];
    scope.downLoadsChart = [];
    scope.viewChart = [];
    scope.shareChart = [];

    scope.loadInfoDashBoardPage = function () {
        services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_data_dash_board_page')}")
            .data({
            })
            .done()
            .then(function (res) {
                debugger
                scope.dashBoard = res;
                var arr_folder = [];
                //////////////////////////////Top 5 Material Category with View/////////////////////////////
                var folder_views = _.map(res.top_five_folder, function (val) {

                    if (val.items.length > 0) {
                        return {
                            folder_id: val.folder_id,
                            //////////count total views in material////////////
                            number: _.reduce(_.map(val.items,function(item){if(item.views){return item.views.length} else{return 0} }), function (memo, num) {
                                return memo + num;
                            })
                        }
                    } else { return { folder_id: val.folder_id, number: 0 } }
                })

                for (var i = 0; i < 5; i++) {
                    var max = _.max(folder_views, function (val) { return val.number; });
                    if (max.number != 0) {
                        scope.dataPie.push(max.number)
                        scope.labelsPie.push(max.folder_id)
                        folder_views = _.reject(folder_views, function (num) { return num.folder_id == _.max(folder_views, function (val) { return val.number; }).folder_id });
                    }

                }
            /////////////Top 5 Learning Material with View /////////////////////////
                for (var i = 0; i < scope.dashBoard.top_five_material.length; i++) {
                    if (scope.dashBoard.top_five_material[i]) {
                        scope.labelsHorizontalBar.push(scope.dashBoard.top_five_material[i].material_name)
                        scope.dataHorizontalBar.push(scope.dashBoard.top_five_material[i].views.length)
                    }
                }
//////////////////////////dynamic chart /////////////////////////////////
                var date_now = moment().format('YYYY-MM-DD')
                for (var j = 0; j < 10; j++) {
                    var download_chart = 0
                    var view_chart = 0
                    var share_chart = 0

                    for (var i = 0; i < scope.dashBoard.dynamic_chart.length; i++) {
                        if (scope.dashBoard.dynamic_chart[i].downloads) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].downloads.length; k++) {
                                scope.dashBoard.dynamic_chart[i].downloads.length
                                var date_created = scope.dashBoard.dynamic_chart[i].downloads[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    download_chart += 1;

                            }
                        }
                        ////////////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].views) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].views.length; k++) {
                                scope.dashBoard.dynamic_chart[i].views.length
                                var date_created = scope.dashBoard.dynamic_chart[i].views[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    view_chart += 1;

                            }
                        }
                        ////////////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].sharing_info) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].sharing_info.length; k++) {
                                scope.dashBoard.dynamic_chart[i].sharing_info.length
                                var date_created = scope.dashBoard.dynamic_chart[i].sharing_info[k].date_created
                                var value_date_created = moment(date_created, 'YYYY-MM-DD')
                                var rangeTime = moment.preciseDiff(date_now, value_date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    share_chart += 1;
                            }
                        }
                        //////////////////////////////
                        if (scope.dashBoard.dynamic_chart[i].sharing_social) {
                            for (var k = 0; k < scope.dashBoard.dynamic_chart[i].sharing_social.length; k++) {
                                scope.dashBoard.dynamic_chart[i].sharing_social.length
                                var date_created = scope.dashBoard.dynamic_chart[i].sharing_social[k].date_created
                                var rangeTime = moment.preciseDiff(date_now, date_created, true)
                                var rangeDay = rangeTime.years * 365 + rangeTime.months * 30 + rangeTime.days
                                if (rangeDay == j)
                                    share_chart += 1;
                            }
                        }

                    }
                    scope.downLoadsChart.push(download_chart)
                    scope.viewChart.push(view_chart)
                    scope.shareChart.push(share_chart)

                }
                var dataSetChart = [
                    {
                        backgroundColor: "rgb(106, 143, 0)",
                        borderColor: "rgb(106, 143, 0)",
                        borderWidth: 1,
                        data: scope.downLoadsChart.reverse(),
                        label: 'Download',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }, {
                        backgroundColor: "rgb(1, 110, 208)",
                        borderColor: "rgb(1, 110, 208)",
                        borderWidth: 1,
                        data: scope.viewChart.reverse(),
                        label: 'View',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }, {
                        backgroundColor: "rgb(226, 113, 54)",
                        borderColor: "rgb(226, 113, 54)",
                        borderWidth: 1,
                        data: scope.shareChart.reverse(),
                        label: 'Share',
                        fill: false,
                        type: 'line',
                        lineTension: 0,
                    }
                ]
                scope.dataSetChart = dataSetChart;

                scope.$applyAsync();
            })
    }

    scope.loadInfoDashBoardPage();
});