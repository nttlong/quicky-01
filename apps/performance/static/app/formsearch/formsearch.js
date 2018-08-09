var lv;
(function (lv) {
    var _FormSearch = (function () {
        var __scope;
        var __alias;
        function _FormSearch(scope, alias) {
            __scope = scope;
            __alias = alias;
            //__scope.$root.$frmSearch = {};
        }

        _FormSearch.prototype.JobWorking = JobWorking;

        function setConfigFrmSearch(title = "", multiCheck = false) {
            __scope.title = title;
            __scope.multi = multiCheck;
            __scope.alias = __alias;
        }

        function JobWorking(ngModel, prop, title, multi) {
            var me = this;
            me.title = title;
            me.path = "commons/FormSearch/JobWorking";
            me.multi = multi;
            me.openDialog = openDialog(me.title, me.path, function () { });
            setConfigFrmSearch(me.title, me.multi);
            __scope.$watch(__alias + '.value', function (val) {
                if (val && ngModel[prop] != val[prop]) {
                    if (me.multi === true) {
                        ngModel[prop] = _.pluck(val, __scope[__alias]['value_field']);
                    } else {
                        ngModel[prop] = val[__scope[__alias]['value_field']];
                    }
                    __scope.$apply();
                }
            })

            return me;
        }

        /**
         * Hàm mở dialog
         * @param {string} title Tittle của dialog
         * @param {string} path Đường dẫn file template
         * @param {function} callback Xử lí sau khi gọi dialog
         */
        function openDialog(title, path, callback) {
            __scope.headerTitle = title;
            dialog(__scope).url(path).done(function () {
                callback();
                //Set draggable cho form dialog
                $dialog.draggable();
            });
        }

        return _FormSearch;
    }());
    lv.FormSearch = function (scope, alias) {
        return new _FormSearch(scope, alias);
    };
})(lv || (lv = {}));
