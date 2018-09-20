
from . repo_config import get_repo_path
def to_excel_file(queryalble,filename):
    import os
    from . import writers
    xlsx = writers.create()
    aggregate = queryalble
    if not hasattr(queryalble,"get_selected_fields"):
        if hasattr(queryalble,"aggregate"):
            aggregate = queryalble.aggregate
            if hasattr(aggregate,"__func__"):
                aggregate=aggregate()
    for x in aggregate.get_selected_fields():
        xlsx.cols(x,x)
    items = aggregate.get_list()
    xlsx.set_data(items)
    full_file_path =os.sep.join([get_repo_path(),filename])
    xlsx.save(full_file_path)

