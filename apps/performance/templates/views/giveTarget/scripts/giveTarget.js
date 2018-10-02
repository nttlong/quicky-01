(function(scope){
    scope.detail = {
        display: false,
        event:{
            onGenerate: function(){
                openDialog('Phát sinh mục tiêu nhân viên', 'giveTarget/form/genGiveTarget', function(){});
            },
            onAdd: function(){
                openDialog('Chi tiết mục tiêu nhân viên', 'giveTarget/form/editGiveTarget', function(){});
            },
            onEdit: function(){

            },
            onDelete: function(){

            }
        }
    }
    scope.toggleDetail = toggleDetail;

    scope.test = "hello";
    scope.$parent.$parent.$parent.onEdit = onEdit;
    scope.$parent.$parent.$parent.onDelete = onDelete;
    scope.$parent.$parent.$parent.onSearch  = function(val){

    }

    function onEdit(){
        toggleDetail();
    }

    function toggleDetail(){
        if(!scope.detail.display){
            $('.hcs-container .zb-page-sidebar .zb-top').hide();
            $('.hcs-container .zb-page-sidebar .zb-left').hide();
            $('.hcs-container .zb-page-sidebar .zb-right').css('width', '100%');
            scope.detail.display = true;
        }else{
            $('.hcs-container .zb-page-sidebar .zb-top').show();
            $('.hcs-container .zb-page-sidebar .zb-left').show();
            $('.hcs-container .zb-page-sidebar .zb-right').css('width', 'calc(100% - 80px)');
            scope.detail.display = false;
        }
    }

    function onDelete(){

    }

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
});