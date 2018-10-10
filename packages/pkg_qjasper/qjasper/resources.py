import requests
import urllib
from . import xml_parser
from . import dm_obj
from . import search_filter
from . search_filter import resource_types,resource_sort_fields

def search(filter):
    if not type(filter) is search_filter.filter:
        raise Exception("The filter must be 'qjasper.search_filter.filter'")
    from . import get_auth
    from . import get_url_server
    url= get_url_server()+"/rest_v2/resources"
    url = url + "?"+filter.__str__()
    ret= requests.get(
        url,
        auth=get_auth(),
        data=dict(
            json=True
        ),

    )
    print ret.url
    total_items=int(ret.headers.get('Total-Count',0))
    items_per_page=int(ret.headers.get('Result-Count',0))
    total_page=0
    if items_per_page>0:
        total_page=total_items/items_per_page+int(total_items) % int(items_per_page)
    retData =[]
    if ret.content!="":
        lst=xml_parser.parse(ret.content)["resources"]["resourceLookup"]
        if type(lst) is list:
            for item in lst:
                retData.append(dm_obj.lazyobject(item))
            return dm_obj.lazyobject(
                items=retData,
                total=total_items,
                page_size=items_per_page,
                pages=total_page
            )
        else:
            return dm_obj.lazyobject(
                items=[dm_obj.lazyobject(lst)],
                total=total_items,
                page_size=items_per_page,
                pages=total_page
            )
    else:
        return dm_obj.lazyobject(
            items=[],
            total=0,
            page_size=0,
            pages=0
        )
def get_info(path):
    from . import get_auth
    from . import get_url_server
    if path[0]=='/':
        path=path[1:path.__len__()]
    url = get_url_server() + "/rest_v2/resources/"+path
    url = url + "?" + filter.__str__()
    ret = requests.get(
        url,
        auth=get_auth(),
        data=dict(
            json=True
        )
    )
    info=xml_parser.parse(ret.content)
    ret_info=dm_obj.lazyobject(info[info.keys()[0]])
    ret_info.__validator__=False
    ret_info.resource_type=info.keys()[0]
    return ret_info
def create_folder(path):
    from . import get_auth
    from . import get_url_server
    if path[0] == '/':
        path = path[1:path.__len__()]
    url = get_url_server() + "/rest_v2/resources/" + path+"?createFolders=True"
    url = url + "?" + filter.__str__()
    ret = requests.post(
        url,
        auth=get_auth(),
        data=dict(
            json=True
        )
    )
    info = xml_parser.parse(ret.content)
    ret_info = dm_obj.lazyobject(info[info.keys()[0]])
    return ret_info