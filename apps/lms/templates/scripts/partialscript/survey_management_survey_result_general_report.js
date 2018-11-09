(function (scope) {
    scope.$onReady(function(){
        
        var scrollBarWidths = 40;
        
        function widthOfListQuestion(){
            var itemsWidth = 0;
            $('.question-list li').each(function () {
                var itemWidth = $(this).outerWidth();
                itemsWidth += itemWidth;
            });
            return itemsWidth;
        };
        function widthOfStepQuestion(){
            var step = $('.question-list li').outerWidth()*3
            return step;
        };
        
         function widthOfHiddenQuestion() {
            return (($('.hcs-scroll-bar-question-container').outerWidth()) - widthOfListQuestion() - getLeftPosiQuestion()) - scrollBarWidths;
        };
    
         function getLeftPosiQuestion() {
            return $('.question-list').position().left;
        };
    
        function reAdjustQuestion() {
            if (($('.hcs-scroll-bar-question-container').outerWidth()) < widthOfListQuestion()) {
                $('.question-scroller-right').show();
            } else {
                $('.question-scroller-right').hide();
            }
    
            if (getLeftPosiQuestion() < 0) {
                $('.question-scroller-left').show();
            } else {
                $('.item').animate({
                    left: "-=" + getLeftPosiQuestion() + "px"
                }, 'slow');
                $('.question-scroller-left').hide();
            }
        }
    
        
        reAdjustQuestion();
        $(window).on('resize', function (e) {
            reAdjustQuestion();
        });
        
        $('.question-scroller-right').click(function () {
            
            var step = 0;
                    $('.question-scroller-left').fadeIn('slow');
                    if(widthOfHiddenQuestion() >=0  ){
                        $('.question-scroller-right').fadeOut('slow');
                    }
                    else
                    {
                     if(widthOfHiddenQuestion() < -widthOfStepQuestion() ){
                       
                       step = -widthOfStepQuestion()
                     }
                      else{
                        step = widthOfHiddenQuestion();
                      }
                        $('.question-list').animate({ left: "+=" + step+ "px" }, 'slow', function ()   {
                
                        });
                    }
                    
        });
    
        $('.question-scroller-left').click(function () {
                
            var step = 0;
            $('.question-scroller-right').fadeIn('slow');
        
            if(getLeftPosiQuestion()>=0  ){
                $('.question-scroller-left').fadeOut('slow');
            }
            else{
             if(getLeftPosiQuestion() < -widthOfStepQuestion() ){
               
               step = -widthOfStepQuestion()
             }
              else{
                step = getLeftPosiQuestion() ;
              }
                $('.question-list').animate({ left: "-=" + step + "px" }, 'slow', function ()      {
        
                });
            }
        
        });
    
   //////////////////////////////////////////
   
    function widthOfList(){
        var itemsWidth = 0;
        $('.question-category-list li').each(function () {
            var itemWidth = $(this).outerWidth();
            itemsWidth += itemWidth;
        });
        return itemsWidth;
    };
    function widthOfStep(){
        var step = $('.question-category-list li').outerWidth()*3
        return step;
    };
    
     function widthOfHidden() {
        return (($('.hcs-scroll-bar-question-category-container').outerWidth()) - widthOfList() - getLeftPosi()) - scrollBarWidths;
    };

     function getLeftPosi() {
        return $('.question-category-list').position().left;
    };

    function reAdjust() {
        if (($('.hcs-scroll-bar-question-category-container').outerWidth()) < widthOfList()) {
            $('.question-category-scroller-right').show();
        } else {
            $('.question-category-scroller-right').hide();
        }

        if (getLeftPosi() < 0) {
            $('.question-category-scroller-left').show();
        } else {
            $('.item').animate({
                left: "-=" + getLeftPosi() + "px"
            }, 'slow');
            $('.question-category-scroller-left').hide();
        }
    }
    reAdjust();
    $(window).on('resize', function (e) {
        reAdjust();
    });
    
    $('.question-category-scroller-right').click(function () {
        
        var step = 0;
                $('.question-category-scroller-left').fadeIn('slow');
                if(widthOfHidden() >=0  ){
                    $('.question-category-scroller-right').fadeOut('slow');
                }
                else
                {
                 if(widthOfHidden() < -widthOfStep() ){
                   
                   step = -widthOfStep()
                 }
                  else{
                    step = widthOfHidden();
                  }
                    $('.question-category-list').animate({ left: "+=" + step+ "px" }, 'slow', function ()   {
            
                    });
                }
                
    });
    $('.question-category-scroller-left').click(function () {   
        var step = 0;
        $('.question-category-scroller-right').fadeIn('slow');
    
        if(getLeftPosi()>=0  ){
            $('.question-category-scroller-left').fadeOut('slow');
        }
        else{
         if(getLeftPosi() < -widthOfStep() ){
           
           step = -widthOfStep()
         }
          else{
            step = getLeftPosi() ;
          }
            $('.question-category-list').animate({ left: "-=" + step + "px" }, 'slow', function ()      {
    
            });
        }
    });
    scope.$watch(function(){
        return scope.$element.find('#myTab1-list-question').html()
},function(n,o){
    if(n!=o){
          
        $('.question-list').css({ left: "-=" + getLeftPosiQuestion() + "px" });
        reAdjustQuestion();
        reAdjust();
        
    }
})
    })
    
    scope.$$display = {
        detail: true
    }
    scope.testDataQuestion =[
        {"category": "First Category", "question":[{"title":"Question 1","content":"This is question 1" },{"title":"Question 2","content":"This is question 2" }] },
        {"category": "Second Category", "question":[{"title":"Question 1","content":"This is question 1" },{"title":"Question 2","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
        {"title":"Question 3","content":"This is question 2" },
    ] },
        {"category": "Third Category", "question":[{"title":"Question 1","content":"This is question 1" },{"title":"Question 2","content":"This is question 2" }] },
        {"category": "Forth Category", "question":[{"title":"Question 1","content":"This is question 1" },{"title":"Question 2","content":"This is question 2" }] },
         
    ]
    scope.$$table = {
        tableFields: [{
                "data": "category_id",
                "title": "${get_res('id','ID')}",
                "className": "text-left"
            },
            {
                "data": "category_name",
                "title": "${get_res('question_category_name','Tên')}",
                "className": "text-left"
            },
            {
                "data": "question_group_display",
                "title": "${get_res('question_group','Nhóm câu hỏi')}",
                "className": "text-left"
            },
            {
                "data": "num_of_questions",
                "title": "${get_res('number_of_questions','Số câu hỏi')}",
                "className": "text-center"
            },
            {
                "data": "created_on",
                "title": "${get_global_res('created_on','Ngày tạo')}",
                "format": "date:" + scope.$root.systemConfig.date_format,
                "className": "text-center"
            },
            {
                "data": "ordinal",
                "width": "50px",
                "title": "${get_global_res('ordinal','Thứ tự')}",
                "className": "text-center"
            },
            {
                "data": "active",
                "width": "50px",
                "title": "${get_res('disabled','Ngưng sử dụng')}",
                "format": "checkbox",
                "className": "text-center"
            }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) {
            scope.onEdit();
        },
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
    scope.opentab = 1;
    scope.selectItem = function (data) {
        scope.opentab = data;

    }
///////////
    scope.currentQuestion = 0;
   

    scope.isSet = function(tabNum){
    return scope.currentQuestion === tabNum;
    };


    scope.chooseQuestion = function (index){
            scope.currentQuestion = index
            
    }
    
    scope.currentCategoryQuestion = 0;
    scope.isSetCategory = function(tabNum){
    return scope.currentCategoryQuestion === tabNum;
    };


    scope.chooseCategoryQuestion = function (index){
        scope.currentQuestion = 0;
            scope.currentCategoryQuestion = index
            scope.$applyAsync();
    }
    /////////////////




    scope.$root.extendToolbar = false;
    scope.dashBoard = {}
    scope.labelSetChart = [];
    (function getLabelDateChart() {
        var arr = [];
        for (var i = 0; i < 5; i++) {
            arr.push(moment().subtract(i, 'd').format('YYYY-MM-DD'));
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
    scope.dataTable = ['50%','70%','20%','50%','80%','10%','100%']
    scope.loadInfoDashBoardPage = function () {
        services.api("${get_api_key('app_main.api.LMSLS_MaterialManagement/get_data_dash_board_page')}")
            .data({})
            .done()
            .then(function (res) {
                debugger
                scope.dashBoard = res;




                var date_now = moment().format('YYYY-MM-DD')
                for (var j = 0; j < 5; j++) {

                    var view_chart = 0


                    for (var i = 0; i < scope.dashBoard.dynamic_chart.length; i++) {
                        ///////////////////////////
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

                        //////////////////////////////


                    }

                    scope.viewChart.push(view_chart)


                }
                var dataSetChart = [{
                    backgroundColor: "rgb(1, 110, 208)",
                    borderColor: "rgb(1, 110, 208)",
                    borderWidth: 1,
                    data: scope.viewChart.reverse(),
                    label: 'View',
                    fill: false,
                    type: 'line',
                    lineTension: 0,
                }]
                scope.dataSetChart = dataSetChart;

                scope.$applyAsync();
            })
    }

    scope.loadInfoDashBoardPage();
});