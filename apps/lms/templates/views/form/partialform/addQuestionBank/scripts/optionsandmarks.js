(function (scope){

    scope.entity = scope.$parent.entity;
    scope.entityofanswer = {};
    scope.__mode = scope.$parent.__mode;//mode quest entity
    scope.mode = 1;//mode answer entity // quest is parent of answers
    scope.$$table = {
        tableSource : _loadDataServerSide,
        tableFields : [
            { "data": "no", "title": "${get_res('No_','No.')}" },
            { "data": "answers", "title": "${get_res('option_content','Option Content')}"},
            { "data": "image", "title": "${get_res('image','Image')}","className":"text-center","expr":function(row, data, func){
            func(function(){
                if(row.image)
                    return "<img style='width:15px;height:17px' src='" + scope.$root.url_static + row.image + "'/>";
                return '';
                });
                return true;
            }},
            { "data": "isCorrect","title":"${get_res('correct_answer','Correct Answer(s)')}","className": "text-center","format":"checkbox"},
            { "data": "if_correct","title":"${get_res('correct_score','Correct Score')}","className":"text-left"},
            { "data": "if_incorrect","title":"${get_res('incorrect_score','Incorrect Score')}","className":"text-left"},
        ],
        onSelectTableRow : function ($row) { onEdit(); },
        selectedItems : [],
        currentItem : {},
        tableSearchText : "",
        refreshDataRow : function(){},
    }

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
    debugger
        /*var sort = {};
        $.each(orderBy, function (i, v) {
            sort[v.columns] = (v.type === "asc") ? 1 : -1;
        });
        sort[orderBy[0].columns] =
            services.api("")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                })
                .done()
                .then(function (res) {

                })*/
        //generate no data and null data
        scope.entity.ques_answers.forEach(function(element,index,arr){
            element.no = index+1;
            element.answers = element.answers ? element.answers : "";
            element.if_correct = element.if_correct ? element.if_correct: 0;
            element.if_incorrect = element.if_incorrect ? element.if_incorrect : 0;
        })
        var data = {
            recordsTotal: scope.entity.ques_answers.length,
            recordsFiltered: scope.entity.ques_answers.length,
            data: scope.entity.ques_answers
        };

        callback(data);
        scope.$$table.currentItem = null;
        scope.$apply();
    }

    scope.event = {
        add : function(){
            scope.mode = 1;
            openDialog("${get_res('add_answer','Add anwser')}", '../form/partialform/addQuestionBank/form/addAnswer', function () { }, "addAnswer");
        },
        edit : function(){
            if(scope.$$table.currentItem){
                scope.mode = 2;
                openDialog("${get_res('Detail_Religion','Chi tiết tôn giáo')}", 'form/partialform/addQuestionBank/form/addAnswer', function () { });
            } else {
                $msg.message("${get_global_res('Notification','Thông báo')}", "${get_app_res('No_Row_Selected','Không có dòng được chọn')}", function () { });
            }
        },
        refresh : function(){

        }
    }

    /**
     * Hàm mở dialog
     * @param {string} title Tittle của dialog
     * @param {string} path Đường dẫn file template
     * @param {function} callback Xử lí sau khi gọi dialog
     * @param {string} id Id của form dialog, default = 'myModal'
     */
    function openDialog(title, path, callback, id = 'myModal') {
    debugger
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
})