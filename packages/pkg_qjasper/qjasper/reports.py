import requests
import urllib
from . import xml_parser
from . import dm_obj
def get_all_report(txt_search=None):
    from . import get_auth
    from . import get_url_server
    url= get_url_server()+"/rest_v2/resources?type=reportUnit&recursive=true"
    if txt_search!=None:
        url=url+"&q="+txt_search
    ret= requests.get(
        url,
        auth=get_auth(),
        data=dict(
            json=True
        ),

    )
    retData =[]
    lst=xml_parser.parse(ret.content)["resources"]["resourceLookup"]
    if type(lst) is list:
        for item in lst:
            retData.append(dm_obj.lazyobject(item))
        return retData
    else:
        return [dm_obj.lazyobject(lst)]
def render_report_to_html(pathToReport,page=None):
    #me.owner.url+"/rest_v2/reports/reports/"+pathToReport+"."+format+"?format="+format#
    from . import get_auth
    from . import get_url_server
    url = get_url_server() + "/rest_v2/reports/"+pathToReport+".html?format=html"
    if page!=None:
        url=url+"&page="+page.__str__()
    ret = requests.get(
        url,
        auth=get_auth()
    )
    if ret.status_code!=200:
        raise Exception(ret.content)
    return ret.content


