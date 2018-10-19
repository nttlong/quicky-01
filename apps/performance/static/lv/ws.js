var _ws_url_
var _wsOnBeforeCall;
var _wsOnAfterCall;
var _ws_export_url_;

var HOMEPAGE_ID = "HOMEPAGE";

function ws_set_export_token_url(url) {
    _ws_export_token_url_ = url;
}
function ws_get_export_token_url() {
    return _ws_export_token_url_;
}
function ws_set_url(url) {
    _ws_url_ = url;
}
function ws_onBeforeCall(callback) {
    _wsOnBeforeCall = callback
}
function ws_onAfterCall(callback) {
    _wsOnAfterCall = callback
}
function ws_get_url() {
    return _ws_url_;
}
function ws_call(api_path, view_path, data, cb, owner, currentFunction) {

    return new Promise(function (resolve, reject) {

        owner.api_path = api_path;
        sender = undefined;
        if (_wsOnBeforeCall) {
            owner.sender = _wsOnBeforeCall();
        }
        var now = new Date();
        var offset_minutes = now.getTimezoneOffset();

        $.ajax({
            url: ws_get_url(),
            type: "post",
            dataType: "json",
            headers: {
                "Function": currentFunction
            },
            data: JSON.stringify({
                path: api_path,
                view: view_path,
                data: data,
                offset_minutes: offset_minutes
            }),
            success: function (res) {
                if (_wsOnAfterCall) {
                    _wsOnAfterCall(owner.sender)
                }
                if (cb) {
                    cb(undefined, res)
                }
                else {
                    resolve(res)
                }

            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (_wsOnAfterCall) {
                    _wsOnAfterCall(owner.sender)
                }
                var txt = jqXHR.responseText
                while (txt.indexOf(String.fromCharCode(10)) > -1) {
                    txt = txt.replace(String.fromCharCode(10), "<br/>")
                }
                if(jqXHR.status === 401){
                    $msg.message(window.common_language.notification, window.common_language.unauthorized, function(){});
                }
                else{
                    $msg.error(window.common_language.internal_server_error, window.common_language.please_try_again_or_contact_with_technical_department, txt, function () { });
                }
            }
        });

    })

}
function ws(scope) {
    function ret(scope) {
        var me = this;

        me.api = function (_api) {
            function ret_api(_api) {
                var _me = this;
                _me._api =   _api;
                _me.data = function (_data) {
                    _me._data = _data;
                    return _me;
                }
                _me.done = function (cb) {
                    if (!scope.view_path) {
                        throw ("view_path is empty")
                    }
                    return ws_call(_me._api, scope.view_path, _me._data, cb, _me, scope.$root.$$$authoriseFunction.id)

                }
            }

            return new ret_api(_api);
        }


    }
    return new ret(scope)
}
