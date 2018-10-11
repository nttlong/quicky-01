function agGridColumn(scope,header,field,type,width){
    if(type=="date"){
        return {
            headerName:header,
            field:field,
            cellRenderer:function(params){
                return scope.$root.$filter('date')(params.getValue(), "dd/MM/yyyy")
                
            }
        }

    }
    else {
        return {
            headerName:header,
            field:field
        }
    }
    
}
