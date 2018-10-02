(function(scope){
    debugger
    console.log(scope);
    scope.$parent.onEdit = null;
    scope.$applyAsync();
    scope.event = {
        onAdd: function(){
            openDialog("Chi tiết mục tiêu", 'updateTarget/form/editUpdateTarget', function(){});
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