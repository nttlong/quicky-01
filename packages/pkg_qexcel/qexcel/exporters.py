def to_excel_file(queryalble,filename):
    from . import writers
    xlsx = writers.create()
    aggregate = queryalble
    if not hasattr(queryalble,"get_selected_fields"):
        if hasattr(queryalble,"aggregate"):
            aggregate = queryalble.aggregate
    for x in aggregate.get_selected_fields():
        xlsx.cols(x,x)
    items = aggregate.get_list()
    xlsx.set_data(items)
    xlsx.save(filename)

