from enum import Enum
import urllib
class resource_types(Enum):
    none=""
    folder="folder"
    jndiJdbcDataSource="jndiJdbcDataSource"
    jdbcDataSource="jdbcDataSource"
    awsDataSource="awsDataSource"
    reportUnit="reportUnit"
    virtualDataSource="virtualDataSource"
    customDataSource="customDataSource"
    beanDataSource="beanDataSource"
    xmlaConnection="xmlaConnection"
    query="query"
    file="file"
    reportOptions="reportOptions"
    semanticLayerDataSource="semanticLayerDataSource"
    domainTopic="domainTopic"
    mondrianConnection="mondrianConnection"
class resource_sort_fields(Enum):
    none=""
    uri="uri"
    label="label"
    description="description"
    type="type"
    creationDate="creationDate"
    updateDate="updateDate"

class filter(object):
    def __init__(self,
                 name_or_description=None,
                 folderUri=None,
                 type=resource_types.none,
                 sortBy=resource_sort_fields.none,
                 page_size=50,
                 page_index=0):
        self.name_or_description=name_or_description
        self.folderUri=folderUri
        self.type=type
        self.sortBy=sortBy
        self.page_size=page_size
        self.page_index=page_index
    def __str__(self):
        return get_str_filter(
            self.name_or_description,
            self.folderUri,
            self.type,
            self.sortBy,
            self.page_size,
            self.page_size*self.page_index
        )


def get_str_filter(name_or_description=None,
           folderUri=None,
           type=resource_types.none,
           sortBy=resource_sort_fields.none,
           limit=50,
           offset=0
):
    # type: (str, str, resource_types, resource_sort_fields) -> object
    """

    :param name_or_description: -> str
    :param folderUri: -> str
    :param type:
    :param sortBy:
    :return:
    """
    ret="limit="+limit.__str__()+"&offset="+offset.__str__()+"&forceFullPage=false&forceTotalCount=true&"
    if name_or_description!=None:
        ret=ret+"q="+(name_or_description)+"&"
    if folderUri!=None:
        ret = ret + "folderUri=" + folderUri + "&"
    if type!=resource_types.none:
        ret = ret + "type=" + (type.__str__()["resource_types.".__len__():type.__str__().__len__()]) + "&"
    if sortBy!=resource_sort_fields.none:
        ret = ret + "sortBy=" + (sortBy.__str__()["resource_sort_fields.".__len__():sortBy.__str__().__len__()]) + "&"
    return ret[0:ret.__len__()-1]




