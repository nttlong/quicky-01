def do_import_data(args):
    import base64
    base64_content = args["data"]["content"]
    data = base64_content.split("base64,")[1]
    buffer_array = base64.decodestring(data)
    pass