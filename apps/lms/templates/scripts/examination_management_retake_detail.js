(function (scope) {
    scope.currentFunction = '';
    scope.mode = 0;
    scope.$display = {
        mapName: [],
        selectedFunction: "",
        selectFunc: function (event, f) {
            scope.$display.selectedFunction = f;
        }
    };

    scope.selectFunc = function (event, f) {
        scope.$display.selectedFunction = f;
    };

    scope.entity = {};
    //scope.backPage = backPage;
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

    function backPage() {
    debugger
        $('.hcs-profile-list').fadeToggle();
        scope.mode = 0;
       // scope.$parent.entity = {};
        setTimeout(function () {
            //scope.$partialpage = scope.$display.mapName[0].url;
            //scope.currentItem = scope.$display.mapName[0].url;
            scope.$display.selectedFunction = scope.$display.mapName[0].function_id;
			scope.$applyAsync();
			$(window).trigger('resize');
		}, 500);
	}

    (function _init_() {
        scope.$display.mapName = scope.$parent.$display.mapName;
        scope.currentFunction = scope.$display.mapName[0];
        scope.$display.selectedFunction = scope.$parent.$display.selectedFunction;
        scope.$applyAsync();
    })();
});