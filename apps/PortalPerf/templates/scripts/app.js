﻿window.set_component_template_url('${get_static("app/directives/")}')
window.set_component_url('${get_static("app/components/")}')
window.set_api_combobox("${get_api_key('app_main.api.common/get_dropdown_list')}")
window.set_authenticated_permission_service("${get_api_key('app_main.api.authenticate_permission/get_permission')}")
window.get_static = "${get_static('/')}"
window.set_static(window.get_static)
angular
    .module("admin", ["c-ui", 'ZebraApp.components', 'ZebraApp.widgets', 'hcs-template', 'authenticatedModule'])
    .controller("admin", controller)
    .filter('$filterFunction', function () {
        return function (input, txtSearch) {
            var output = [];
            _.each(input, function (val) {
                _.each(val.child_items, function (child) {
                    if (child.default_name.toLowerCase().indexOf(txtSearch.toLowerCase()) != -1)
                        if (!_.findWhere(output, val))
                            output.push(val);
                })
            })
            return output;
        };
    })
    .filter('trustAsHtml', ['$sce', function ($sce) {
        return function (text) {
            return $sce.trustAsHtml(text);
        };
    }]);

app.directive('ngRightClick', function($parse) {
    return function(scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function(event) {
            scope.$apply(function() {
                event.preventDefault();
                fn(scope, {$event:event});
            });
        });
    };
});

controller.$inject = ["$dialog", "$scope", "$filter"];
dialog_root_url('${get_app_url("pages/")}')
<%
    import json
%>
function controller($dialog, $scope, $filter) {
    window.top.PYUrl = window.location.origin + '/lms'
    window.top.UIUrl = window.location.origin + '/HoiThao'
    window.top.ServiceUrl = window.location.origin + '/HoiThao_WS'
    window.top.SettingUrl = window.location.origin + '/HoiThaoPortal'
    $scope.$root.$$absUrl = window.location.href;
    $scope.$root.title = "";

    $scope.isHomePage = true;
    $scope.$root.$$absUrl = window.location.href;
    $scope.$root.url_static = "${get_static('/')}";
    $scope.$root.systemConfig = null;/*HCSSYS_SystemConfig*/
    $scope.$root.language = "${get_language()}";
    $scope.$root.APP_URL = "${get_app_url('')}";
    $scope.$root.languages = ${ json.dumps(get_languages()) };
    $scope.VIEW_ID = "${register_view()}"
    $dialog($scope)
    ws_set_url("${get_app_url('api')}")
    ws_set_export_token_url("${get_api_key('app_main.excel.manager/generate_token')}");
    ws_onBeforeCall(function () {
        mask = $("<div class='mask'></div>")
        mask.appendTo("body");
        return mask
    });
    ws_onAfterCall(function (mask) {
        mask.remove();
    })
    history_navigator($scope.$root);

    $scope.view_path = "${get_view_path()}";
    $scope.services = services = ws($scope);
    $scope.$root.$getComboboxData = extension().getComboboxData;
    $scope.$root.$getInitComboboxData = extension().getInitComboboxData;
    $scope.$root.$extension = extension();
    $scope.$root.$groupingNumber = function (num){
        var info = $scope.$root.systemConfig;
        var NumberGroupSeparator = info.dec_place_separator === "," ? "." : ",";
        var NumberDecimalSeparator = info.dec_place_separator === "," ? "," : ".";
        var str = num.toString().split('.');
        if(str[0].length >= 4) {
            str[0] = str[0].replace(/(\d)(?=(\d{3})+$)/g, '$1' + NumberGroupSeparator);
        }
        if(str[1] && str[1].length >= 4) {
            str[1] = str[1].replace(/(\d{3})/g, '$1');
        }
        return str.join(NumberDecimalSeparator);
    };
    $scope.$root.$formatSystem = {
        "number": function(data){
            if(!data){
                return "";
            }
            else if(Number(data) === data && data % 1 !== 0){
                return formatNumber(data);
            }
            else if(Number(data) === data && data % 1 === 0){
                return $scope.$root.$groupingNumber(data);
            }else{
                return "";
            }
        },
        "date": function(data){
            return $filter('date')(data, $scope.$root.systemConfig.date_format);
        }
    }

    window.NumberFormat = {
        "format": function(data){
            formatNumber(data);
        }
    }
    window.DateFormat = {
        "format": $filter('date')
    };
    $scope.$root.collapseSubMenu = function collapseSubMenu(e) {
        e.stopPropagation();
        $('#hcs-top-bar-menu ul li ul').slideUp();
        if (($(e.currentTarget.parentElement.children[1]).css('display') != 'block')) {
            $(e.currentTarget.parentElement.children[1]).slideDown(500);
        }
    };

    $("#btnShowMessage").unbind("click");
    $("#btnShowMessage").bind("click", function () {
        $(this).siblings(".hcs-message-list").toggleClass("message-hidden");
        event.stopPropagation();
    });
    $("#btnShowMenu").unbind("click");
    $("#btnShowMenu").bind("click", function () {
        $(this).siblings(".hcs-menu-list").toggleClass("menu-hidden");
        event.stopPropagation();
    });
    $(window).bind("click", function (e) {
        var isMenu = $(e.target).closest(".hcs-menu-list").length > 0;
        var isMessage = $(e.target).closest(".hcs-message-list").length > 0;
        if (!isMenu && !isMessage) {
            $("#btnShowMenu").siblings(".hcs-menu-list").addClass("menu-hidden");
            $("#btnShowMessage").siblings(".hcs-message-list").addClass("message-hidden");
        }
        if($(".custom-menu").css("display") == "block"){
            $(".custom-menu").css("display", "none")
        }
    });

    // Responsive

    window.onclick = function(ev){
        if(window.innerWidth <= 768){
            if(!ev.target.closest('.hcs-left-side-department-content') && !ev.target.closest('.hcs-menu-mobile')
            && !ev.target.closest('.hcs-toggle-slider')){
                if($('.hcs-left-side-department-content').css('display') == 'block'){
                    $('.hcs-left-side-department-content').toggle('slide');
                }

                if($('.modal-dialog .hcs-left-side-department-content').css('display') == 'block'){
                    $('.modal-dialog .hcs-left-side-department-content').toggle('slide');
                }
            }
        }
    };

    window.onresize  = function(){
        if($('.hcs-left-side-department-content').css('display') == 'none' && window.innerWidth >= 768){
            $('.hcs-left-side-department-content').toggle('slide');
        }

        if($('.hcs-top-action-large').css('display') == 'none' && window.innerWidth >= 768){
            $('.hcs-top-action-large').toggle('slide');
        }
    }

    $scope.$root.doToggle = function(className, event) {
        if(!event){
            $(className).toggle("slide");
        }else{
            $(event.target).closest(".zb-top").find(".zb-right-content").toggle("slide");
        }
    }

    // End Responsive

    $scope.$root.doLogout = function () {
        $scope.$root.__USER__ = null;
        window.location = "${get_app_url('logout')}";
    }

    $scope.slideToggle = function (event) {
        _.forEach($(".hcs-menu-list-group > .hcs-message-group").find(".hcs-menu-group-content"), function (i, v) {
            if ($(i).css("display") !== 'none') {
                $(i).slideToggle(300);
            }
        })
        $(event.target).closest('.hcs-message-group').find('.hcs-menu-group-content').slideToggle(300)
    }
    ////Đồng hồ
    $scope.$root.timer = {
        clock: Clock(),
        meridiem: getMeridiem(),
        date: Calendar()
    };
    setInterval(function () {
        $scope.$root.timer.clock = Clock();
        if ($scope.$root.timer.clock === "00:00") {
            $scope.$root.timer.date = Calendar();
            $scope.$root.timer.meridiem = getMeridiem();
        }
        $scope.$root.$applyAsync();
    }, 100);

    //getTime($scope);

    $(window).on('click', function (e) {
        if (!e.target.closest('#dropdownFunction'))
            $('#dropdownFunction').collapse('hide');
    });

    document.addEventListener("keydown", function (evt) {
        if (evt.ctrlKey && evt.shiftKey && evt.code === "KeyF") {
            $scope.searchFunctionTitle = "${get_global_res('function_list','Danh sách tính năng')}"
            dialog($scope).url("commons/SearchFunction/SearchFunction").done(function () {
                setTimeout(function () {
                    $('#hcs-search-function').find('input').focus();
                }, 1000)
            });
        }
    });

    $scope.$root.$dataPin = {};
    $scope.$root.decrement = function (data, event){
        // Avoid the real one
        event.preventDefault();
        $scope.$root.$dataPin = data;
        $scope.$root.$applyAsync();
        console.log($scope.$root.$dataPin)
        // Show contextmenu
        if($(event.target).closest(".hcs-function-style").length > 0) {
            if($(".custom-menu").css("display") == "none"){
                $(".custom-menu").toggle(100).
                css({
                    top: (event.pageY ) + "px",
                    left: event.pageX + "px"
                });
            } else {
                $(".custom-menu").css("display", "none");
                $(".custom-menu").toggle(100).
                css({
                    top: (event.pageY ) + "px",
                    left: event.pageX + "px"
                });
            }
        }
    }

    $scope.$root.PinTab = function(){
        services.api("${get_api_key('app_main.api.SYS_FunctionList_Favorite/insert')}")
            .data({
                data: $scope.$root.$dataPin
            })
            .done()
            .then(function (res) {
                //set hcssys_systemconfig
                var data = $scope.$root.$functions;
                for(var i = 0; i < data.length; i++) {
                    var childs = data[i]["child_items"];
                    for(var j = 0; j < childs.length; j++) {
                        if(childs[j]["function_id"] == $scope.$root.$dataPin["function_id"]) {
                            childs[j]["favorites"] = true;
                            break;
                        }
                    }
                }
                $scope.$root.systemconfig = res;
            })
    }

    $scope.$root.UnPinTab = function(){
        services.api("${get_api_key('app_main.api.SYS_FunctionList_Favorite/delete')}")
            .data({
                data: $scope.$root.$dataPin
            })
            .done()
            .then(function (res) {
                //set hcssys_systemconfig
                var data = $scope.$root.$functions;
                for(var i = 0; i < data.length; i++) {
                    var childs = data[i]["child_items"];
                    for(var j = 0; j < childs.length; j++) {
                        if(childs[j]["function_id"] == $scope.$root.$dataPin["function_id"]) {
                            childs[j]["favorites"] = false;
                            break;
                        }
                    }
                }
                $scope.$root.systemconfig = res;
            })
    }

    $scope.setTitle = function(){
        if($scope.$root.currModule.module_name) {
            document.title = $scope.$root.currModule.module_name;
        }else{
            setTimeout(function(){
                $scope.setTitle();
            }, 100);
        }
    }

    $scope.$root.clickUrl = function(data){
        console.log(data)
        var url = data.redirect_url;
        if(url){
            url = url.replace("$C_UI", window.top.UIUrl)
                            .replace("$C_WS", window.top.ServiceUrl)
                            .replace("$C_APP", window.top.SettingUrl)
                            .replace("$P_UI", window.top.PYUrl);
            if(data.is_new_tab){
                window.open(url, '_blank');
            } else {
                window.location.href = url;
            }
        }
    }

    function formatNumber(data){
        var dataFormatSeperator = $scope.$root.$groupingNumber(data);
        var NumberDecimalSeparator = $scope.$root.systemConfig.dec_place_separator === "," ? "," : ".";
        var leng = $scope.$root.systemConfig.dec_place_currency - dataFormatSeperator.substring(dataFormatSeperator.lastIndexOf($scope.$root.systemConfig.dec_place_separator) + 1, dataFormatSeperator.length).length;

        var lenDec = dataFormatSeperator.substring(dataFormatSeperator.lastIndexOf($scope.$root.systemConfig.dec_place_separator) + 1, dataFormatSeperator.length).length;

        function retData(data, len){
            for(var i = 0; i < len; i++){
                data += "0";
            }
            return data;
        }

        if(lenDec > $scope.$root.systemConfig.dec_place_currency){
            var data = retData(dataFormatSeperator, leng);
            return data.substring(0, data.lastIndexOf(NumberDecimalSeparator) + $scope.$root.systemConfig.dec_place_currency + 1);
        }

        return retData(dataFormatSeperator, leng);
    }

    /**
     * Initialize Data
     */
    function activate() {
        $scope.$root.currentFunction = {};
        $scope.$root.$$$authoriseFunction  = {
            id: "HOME"
        };
        $scope.$root.currentModule = '';
        $scope.$root.currModule = {};
        $scope.$root.logo = "${get_static('/')}css/images/logo.png";

        //Get function list
        services.api("${get_api_key('app_main.api.functionlist/get_list')}")
            .data({
                //parameter at here
                language: "${request.get_language()}"
            })
            .done()
            .then(function (res) {
                var functions = JSON.parse(JSON.stringify(res));
                /**
                 * Customize string tittle group when display data
                 */
                $.each(res, function (idx, val) {
                    if (val.parent_id == null) {
                        var arr = val["custom_name"] ? val["custom_name"].split("/") : "";
                        if(arr && arr.length > 1){
                            var display_name = arr[0];
                            var display_name_bold = arr[1];
                            val["display_name"] = display_name;
                            val['display_name_bold'] = display_name_bold;
                        }
                    }
                });

                /**
                 * Function list
                 */
                $scope.$root.$function_list = functions;

                var fs_module = _.filter(res, function (d) {
                    return d["parent_id"] == -1;
                });

                $scope.$$$fs_module = fs_module;

                var fs = _.filter(res, function (d) {
                    return d["parent_id"] == null;
                });
                $.each(fs, function (idx, val) {
                    val["child_items"] = _.filter(res, function (d) {
                        return d["parent_id"] == val["function_id"] && d["active"] == true;
                    });
                });
                $scope.$root.$functions = fs;
                $scope.$applyAsync();
                $scope.$root.getPage = function () {
                    return (angular.isObject($scope.$root.currentFunction))
                        ? "${get_app_url('')}/pages/" + $scope.$root.currentFunction.url
                        : "${get_app_url('')}/pages/home";
                }
                $scope.$root.$history.change(function (data) {
                    $scope.$root.$$absUrl = window.location.href;
                    if (data.page) {
                        if(!_.findWhere($scope.$root.$function_list, {function_id:data.page}))
                        {
                            data.page = $scope.$root.$extension.TripleDES.decrypt(data.page);
                            if(data.f)
                                data.f = $scope.$root.$extension.TripleDES.decrypt(data.f);
                        }
                        $scope.isHomePage = false;
                        var currentFunction = _.filter(functions, function (d) {
                            return d["function_id"] == data.page;
                        });
                        if (currentFunction.length > 0) {
                            //Set current function
                            $scope.$root.currentFunction = currentFunction[0];
                            $scope.$root.currentModule = _.filter(functions, function (d) {
                                return d["function_id"] == currentFunction[0].parent_id;
                            })[0];
                            document.title = $scope.$root.currentModule.custom_name_lb;
                        }
                    } else {
                        $scope.$root.currentFunction = $scope.$root.currentModule = null;
                        $scope.setTitle();
                        $scope.isHomePage = true;
                    }
                    $scope.$root.$applyAsync();
                })
            })

        //Get HCSSYS_SystemConfig
        services.api("${get_api_key('app_main.api.HCSSYS_SystemConfig/get_config')}")
            .data({
                //parameter at here
            })
            .done()
            .then(function (res) {
                //Set HCSSYS_SystemConfig

                $scope.$root.systemConfig = res;
            })

        //Current user
        services.api("${get_api_key('app_main.api.auth_user/get_user_info_by_user_name')}")
            .data({
                "username": "${get_user()}"
            })
            .done()
            .then(function (res) {
                //Set HCSSYS_SystemConfig
                $scope.$root.__USER__ = res;
            })

            //Get Module Navigation
        services.api("${get_api_key('app_main.api.functionlist/get_list_module')}")
            .data({
                language: "${request.get_language()}"
            })
            .done()
            .then(function (res) {
                var modules = _.filter(res, function(v){
                    return v.module_code.toLocaleLowerCase() != "perf";
                })

                var curr_module = _.filter(res, function(v){
                    return v.module_code.toLocaleLowerCase() == "perf";
                })

                $scope.$root.currModule.module_name = (curr_module && curr_module.length > 0 )? curr_module[0].custom_name : "";

                if(/\r|\n/.exec($scope.$root.currModule.module_name)) {
                    $scope.title1 = $scope.$root.currModule.module_name.split("\n")[0];
                    $scope.title2 = $scope.$root.currModule.module_name.split("\n")[1];
                } else {
                    $scope.title2 = $scope.$root.currModule.module_name;
                }

                //$scope.$root.title = $scope.$root.currModule.module_name;
                $scope.$root.$$$list_modules = modules;
                window.top.dataInfo = {};
                window.top.dataInfo.listModule = res;
            })
    }
    /**
     * Init
     */
    activate();
}

function getTime($scope) {
    moment.lang('${get_language()}');

    $scope.$$$dateTime = {
        $$$date: toTitleCase(moment()["format"]("dddd, D MMMM, YYYY")),
        $$$hour: moment()["format"]("hh:mm"),
        $$$clock: moment()["format"]("a").toLocaleUpperCase()
    }

    setTimeout(getTime($scope), 1000);

    $scope.$applyAsync();
}

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) { return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase(); });
}

function extension() {
    var fac = {};

    fac.guid = function () {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    };

    fac.getComboboxData = getComboboxData;
    fac.getInitComboboxData = getInitComboboxData;
    fac.openDialog = openDialog;
    fac.getValueList = getValueList;
    fac.TripleDES = {
        _password: CryptoJS.MD5("lv"),
        setPassword: function(password){
            fac.TripleDES._password = CryptoJS.MD5(password);
        },
        encrypt: function(val){
            try {
                fac.TripleDES._password.words[4] = fac.TripleDES._password.words[0];
                fac.TripleDES._password.words[5] = fac.TripleDES._password.words[1];

                // create a 64-bit zero filled
                var iv = CryptoJS.lib.WordArray.create(64/8);
                return CryptoJS.TripleDES.encrypt(val, fac.TripleDES._password, {iv: iv}).toString();
            }
            catch(err) {
                throw err
            }
        },
        decrypt: function(val){
            try {
                fac.TripleDES._password.words[4] = fac.TripleDES._password.words[0];
                fac.TripleDES._password.words[5] = fac.TripleDES._password.words[1];
                var ct = {
                    ciphertext: CryptoJS.enc.Base64.parse(val)
                };
                var iv = CryptoJS.lib.WordArray.create(64/8);
                var decrypted = CryptoJS.TripleDES.decrypt(ct, fac.TripleDES._password, {iv: iv});
                return decrypted.toString(CryptoJS.enc.Utf8);
            }
            catch(err) {
                throw err
            }
        }
    };

    /**
     * [openDialog description]
     * @param  {[type]}   scope    [description]
     * @param  {[type]}   title    [description]
     * @param  {[type]}   path     [description]
     * @param  {Function} callback [description]
     * @param  {String}   id       [description]
     * @return {[type]}            [description]
     */
    function openDialog(scope, title, path, callback, id = 'myModal') {
        if ($('#' + id).length === 0) {
            scope.headerTitle = title;
            dialog(scope).url(path).done(function () {
                callback();
                $dialog.draggable();
            });
        }
    }

    function getValueList(param, fnCallBack){
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                name: param
            })
            .done()
            .then(function (res) {
                fnCallBack(res);
            });
    }

    /**
     * Hàm get combobox data
     * @param {object} scope
     * @param {void} cbSetData
     * @param {number} pgIdx
     * @param {string} txtSearch
     */
    function getComboboxData(scope, cbSetData, pgIdx, txtSearch) {
        services.api("${get_api_key('app_main.api.common/get_combobox_data')}")
            .data({
                //parameter at here
                "key": scope.params.key,
                "value": scope.params.value,
                "pageIndex": pgIdx - 1,
                "search": txtSearch,
            })
            .done()
            .then(function (res) {
                scope.captionField = res.caption_field;
                scope.keyField = res.value_field;
                scope.title = res.display_name;
                scope.templateFields = res.display_fields;
                var data = {};
                if (res.hasOwnProperty('parent_field') && res['parent_field']) {
                    data = res.data.items;
                }
                else {
                    data = {
                        recordsTotal: res.data.total_items,
                        data: res.data.items
                    };
                }
                cbSetData(data);
            });
    }

    /**
     * Hàm get data init combobox
     * @param {object} scope
     * @param {any} key Trường hợp get nhiều truyền tham số là array object
     * example:[{key:xxx, code:xxx}, {key:yyy, code:yyy}]
     * Trường hợp get đơn lẻ truyền tham số là object
     * example:{key:xxx, code:xxx}
     */
    function getInitComboboxData(scope, key, callback) {
        services.api("${get_api_key('app_main.api.common/get_init_data_combobox')}")
            .data({
                name: key
            })
            .done()
            .then(function (res) {
                if (angular.isArray(res)) {
                    $.each(res, function (i, v) {
                        scope[v.alias] = v;
                    });
                } else {
                    scope[res.alias] = res;
                }
                if(callback) callback();
                scope.$applyAsync();
            })
    }

    return fac;
};

function Clock() {
    return moment().locale("${get_language()}").format("HH:mm");
}

function toStartCase(str) {
    return str
        .toLowerCase()
        .split(' ')
        .map(function (word) {
            return word[0].toUpperCase() + word.substr(1);
        })
        .join(' ');
}

function Calendar() {
    moment.lang("${get_language()}" == "vn" ? "vi" : "${get_language()}");
    return toStartCase(moment().locale("${get_language()}").format('dddd, DD MMMM, YYYY'));
}

function getMeridiem() {
    return moment().locale("${get_language()}").format("a");
}

window.common_language = {
    "notification" : "${get_global_res('notification','Thông báo')}",
    "unauthorized" : "${get_global_res('unauthorized','Không được phép')}",
    "internal_server_error" : "${get_global_res('Internal_Server_Error','Có lỗi từ phía máy chủ')}",
    "please_try_again_or_contact_with_technical_department" : "${get_global_res('please_try_again_or_contact_with_technical_department','Xin vui lòng thử lại hoặc liên hệ bộ phận kỹ thuật')}"
}