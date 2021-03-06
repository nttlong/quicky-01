﻿(function (scope) {
    scope.$$table = {
        tableFields: [
            { "data": "approve_level", "title": "${get_res('approve_level','Số cấp duyệt')}" },
            { "data": "approver_value_display", "title": "${get_res('approver_value_display','Người duyệt')}" },
            { "data": "email_approve_code", "title": "${get_res('email_approve_code','Email duyệt')}" },
            { "data": "email_approve_to_name", "title": "${get_res('email_approve_to','Gửi tới')}" },
            { "data": "email_reject_code", "title": "${get_res('email_reject_code','Email không duyệt')}" },
            { "data": "email_reject_to_name", "title": "${get_res('email_reject_to','Gửi tới')}" },
            { "data": "toolbar", "title": "", "className": "text-center", "expr": function(row, columns, func){
                if(scope.$root){
                    var guid = scope.$root.$extension.guid();
                    func(function(){
                        return "<button style='background: none;border: none;color: #37a5dd;' id='" + guid +"'><i class='bowtie-icon bowtie-edit-outline'></i></button>";
                    });
                    $(document).ready(function(){
                        $('#' + guid).bind('click', function(event){
                            $(event.currentTarget.closest('tr')).dblclick();
                        });
                    })
                    return true;
                }
                return false;
            }, "visible": scope.$root ? true : false }
        ],
        $$tableConfig: {},
        tableSource: _loadDataServerSide,
        onSelectTableRow: function ($row) { onEdit(); },
        selectedItems: [],
        currentItem: {},
        tableSearchText: "",
        refreshDataRow: function () { /*Do nothing*/ }
    };
    scope.__mode = scope.$parent.$parent.$parent.$parent.mode;
    scope.LSendMail = [];
    scope.LScoreBy = [];
    scope.$$process_id = scope.__mode == 2 ? scope.$parent.$parent.$parent.$parent.$$table.currentItem.process_id : null;
    scope.$$curr_max_approve_level = scope.__mode == 2 ? JSON.parse(JSON.stringify(scope.$parent.$parent.$parent.$parent.$$table.currentItem.max_approve_level)) : 0;
    //debugger
    //scope.$parent.$parent.$parent.$parent.onAdd = onAdd;

    scope._tableData = _tableData;
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
            services.api("${get_api_key('app_main.api.TM_SetupProcessApproveLevel/get_list_approve_level_by_process_id')}")
                .data({
                    //parameter at here
                    "pageIndex": iPage - 1,
                    "pageSize": iPageLength,
                    "search": searchText,
                    "sort": sort,
                    "process_id": scope.$$process_id
                })
                .done()
                .then(function (response) {
                    _.each(response.items, function(val){
                        val.toolbar = true;
                    })
                    var data = {};
                    if(!scope.LSendMail || scope.LSendMail.length === 0){
                        _getListValueList("LSendEmail", function(res){
                            scope.LSendEmail = res.values;
                            _.each(response.items, function(valItems){
                                if(valItems['email_approve_to'] && valItems['email_approve_to'].length > 0){
                                    var displayEmailApprove = [];
                                    _.each(valItems['email_approve_to'], function(valApprove){
                                        displayEmailApprove.push(_.findWhere(scope.LSendEmail, {"value":valApprove}).caption);
                                    });
                                    valItems['email_approve_to_name'] = displayEmailApprove.join(", ");
                                }else{
                                    valItems['email_approve_to_name'] = "";
                                }
                                if(valItems['email_reject_to'] && valItems['email_reject_to'].length > 0){
                                    var displayEmailReject = [];
                                    _.each(valItems['email_reject_to'], function(valReject){
                                        displayEmailReject.push(_.findWhere(scope.LSendEmail, {"value":valReject}).caption);
                                    });
                                    valItems['email_reject_to_name'] = displayEmailReject.join(", ");
                                }else{
                                    valItems['email_reject_to_name'] = "";
                                }
                            });
                            data = {
                                recordsTotal: response.total_items,
                                recordsFiltered: response.total_items,
                                data: response.items
                            };
                            callback(data);
                            scope.$$table.currentItem = null;
                            scope.$apply();
                        })
                    }else{
                        _.each(response.items, function(valItems){
                                if(valItems['email_approve_to'] && valItems['email_approve_to'].length > 0){
                                    var displayEmailApprove = [];
                                    _.each(valItems['email_approve_to'], function(valApprove){
                                        displayEmailApprove.push(_.findWhere(scope.LSendEmail, {"value":valApprove}).caption);
                                    });
                                    valItems['email_approve_to_name'] = displayEmailApprove.join(", ");
                                }else{
                                    valItems['email_approve_to_name'] = "";
                                }
                                if(valItems['email_reject_to'] && valItems['email_reject_to'].length > 0){
                                    var displayEmailReject = [];
                                    _.each(valItems['email_reject_to'], function(valReject){
                                        displayEmailReject.push(_.findWhere(scope.LSendEmail, {"value":valReject}).caption);
                                    });
                                    valItems['email_reject_to_name'] = displayEmailReject.join(", ");
                                }else{
                                    valItems['email_reject_to_name'] = "";
                                }
                            });
                            data = {
                                recordsTotal: response.total_items,
                                recordsFiltered: response.total_items,
                                data: response.items
                            };
                            callback(data);
                            scope.$$table.currentItem = null;
                            scope.$apply();
                    }
                })
    }
    scope.$parent.$parent.$parent.onSearch= null;
    scope.$parent.$parent.$parent.onAdd = null;
    //scope.$parent.$parent.$parent.$parent.onEdit = null
    scope.$parent.$parent.$parent.onDelete = null;
    scope.$parent.$parent.$parent.onImport = null;
    scope.$parent.$parent.$parent.onExport = null;
    scope.$parent.$parent.$parent.onEdit = null;
    scope.$parent.$parent.$parent.onSave = null;

    function onEdit() {
        if (scope.$$table.currentItem) {
            scope.mode = 2; // set mode chỉnh sửa
            openDialog("${get_res('approver_level_detail','Chi tiết Cấp duyệt')}", 'setup_process/setup_process_detail/form/addApproverLevel', function () { });
        }
    };

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

    function _getListValueList(parameter, callback) {
        //valuelist
        services.api("${get_api_key('app_main.api.SYS_ValueList/get_list')}")
            .data({
                "name": parameter
            })
            .done()
            .then(function (res) {
                callback(res);
            })
    }
});