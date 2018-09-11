import threading
from bson import ObjectId
import re
global __apps_views_cache__
global __revert_apps_views_cache__
global __lock__
__lock__ = threading.Lock()
__apps_views_cache__ = {}
__revert_apps_views_cache__ ={}
def get_view_id(coll,appname,viewpath,file,page_caption=None,parent_view_path=None,is_public=False,privileges=None):
    viewpath =viewpath.lower()
    appname = appname.lower()

    key ="app={0};view={1}".format(appname,viewpath).lower()
    if __apps_views_cache__.has_key(key):
        return __apps_views_cache__[key]
    else:
        __lock__.acquire()
        try:
            if page_caption == None:
                page_caption = viewpath
            default_privileges = ["view","insert","update","delete","print","import_excel","export_excel"]
            if privileges!=None:
                default_privileges.extend(privileges)
            item =coll.find_one({
                "app":{"$regex": re.compile("^"+appname+"$")},
                "view":{"$regex": re.compile("^"+viewpath+"$")}
            })
            if item == None:
                if parent_view_path!=None:
                    parent_key = "app={0};view={1}".format(appname,parent_view_path).lower()
                    parent_item =coll.find_one({
                        "full_path":{
                            "$regex":re.compile("^"+parent_key+"$")
                        }
                    })
                    _paths_ = []
                    if parent_item!=None:
                        _paths_ = parent_item["paths"]
                    _paths_.extend([viewpath.lower()])
                    ret = coll.insert_one({
                        "app":appname,
                        "view":viewpath,
                        "privileges":default_privileges,
                        "is_public":is_public,
                        "full_path":key,
                        "parent":parent_key,
                        "caption":page_caption,
                        "paths":_paths_,
                        "file":file

                    })
                else:
                    ret = coll.insert_one({
                        "app": appname,
                        "view": viewpath,
                        "privileges": default_privileges,
                        "is_public": is_public,
                        "full_path": key,
                        "caption":page_caption,
                        "paths":[viewpath.lower()],
                        "file": file

                    })
                __apps_views_cache__.update({
                    key:ret.inserted_id.__str__()
                })
                __revert_apps_views_cache__.update({
                    ret.inserted_id.__str__():dict(
                        app=appname,
                        view = viewpath
                    )
                })
            else:
                __apps_views_cache__.update({
                    key: item["_id"].__str__()
                })
                if is_public != item["is_public"]:
                    coll.update_one({
                        "_id":item["_id"]},{
                        "$set":{
                            "is_public":is_public
                        }
                    })
                if set(item["privileges"])!=set(default_privileges):
                    coll.update_one({
                        "_id": item["_id"]},{
                        "$set": {
                            "privileges":default_privileges
                        }
                    })
                if parent_view_path!=None:
                    parent_key = "app={0};view={1}".format(appname,parent_view_path).lower()
                    parent_item = coll.find_one({
                        "full_path": {
                            "$regex": re.compile("^" + parent_key + "$")
                        }
                    })
                    _paths_ = parent_item["paths"]
                    _paths_.append(viewpath.lower())
                    if set(_paths_) != set(item["paths"]):
                        coll.update_one({
                            "_id": item["_id"]},{
                            "$set": {
                                "paths": _paths_
                            }
                        })
                elif item.get("parent",None)!=None:
                    coll.update_one({
                        "_id": item["_id"]},
                        {
                        "$unset": {
                            "parent": None
                        }
                    })
                    coll.update_one({
                        "_id": item["_id"]},
                        {
                            "$set": {
                                "paths": [viewpath]
                            }
                        })



                __revert_apps_views_cache__.update({
                    item["_id"].__str__().__str__(): dict(
                        app=appname,
                        view=viewpath
                    )
                })
            __lock__.release()
            return __apps_views_cache__[key]
        except Exception as ex:
            __lock__.release()
            raise ex

def get_view_info_from_id(coll,id):
    if __revert_apps_views_cache__.has_key(id):
        return __revert_apps_views_cache__[id]
    else:
        __lock__.acquire()
        try:
            item = coll.find_one({
                "_id":ObjectId(id)
            })
            if item == None:
                raise (Exception("view with id '{0}' was not found".format(id)))
            else:
                __revert_apps_views_cache__.update({
                    id:dict(
                        app=item["app"],
                        view = item["view"]
                    )
                })
                key = "app={0};view={1}".format(item["app"], item["view"]).lower()
                __apps_views_cache__.update({
                    key:id
                })
            __lock__.release()
            return __revert_apps_views_cache__[id]
        except Exception as ex:
            __lock__.release()
            raise ex
