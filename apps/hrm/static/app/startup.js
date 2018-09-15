
function startup(baseUrl,callback){
    window.appReady=callback;
    var settings={
        shim:{},
        baseUrl:baseUrl,
        paths:{},
        load:function(id,url){
            console.log(id);
            console.log(url);
        }
    }
    var requires=[]
    var revertRequire={}

    for(var i=0;i<scripts.items.length;i++){
        settingItem={}
        _script = scripts.items[i];
        tmpScriptPath=_script.substring(0,_script.length-3);
        settings.paths["scripts_"+i]=tmpScriptPath
        requires.push("scripts_"+i);
        revertRequire[_script]="scripts_"+i;
    }
    var shim ={};
    for(var i=0;i<scripts.ref.length;i++){
        var item =scripts.ref[i];
        
        for(var j=0;j<item.items.length;j++){
            var key =revertRequire[item.items[j]];
            if(key==undefined){
                var _script = item.items[j];
                var tmpScriptPath=_script.substring(0,_script.length-3);
                
                key="scripts_"+requires.length;
                requires.push(key)
                revertRequire[_script]=key;
                settings.paths[key]=tmpScriptPath;
            }
            if(!shim[key]){
                shim[key]={deps:[]};
            }
            var refPath=revertRequire[item.src];
            if(refPath==undefined){
                var _script = item.src;
                var tmpScriptPath=_script.substring(0,_script.length-3);
                
                var _key="scripts_"+requires.length;
                requires.push(_key)
                revertRequire[_script]=_key;
                settings.paths[_key]=tmpScriptPath;
            }
            if(!shim[key]){
                throw(key);
            }
            shim[key].deps.push(revertRequire[item.src]);
            
        }
    }
    shim["app"]={
        deps:[]
    }
    for(var i=0;i<requires.length;i++){
        shim["app"].deps.push(requires[i])
    }
    requires.push("app");
    settings.paths["app"]="app/app";
    console.log(settings);
    settings.shim=shim;
    require.config(settings);
    require(requires,function(){
        
        
    });
}
