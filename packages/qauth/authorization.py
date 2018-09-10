from . import authorize
class auth(object):
    def process_request(selfs,request):
        from django.conf import settings
        authorize.authorize.create_app(request.__app__.name)
        if request.get_schema()!=None:
            authorize.authorize.app_add_schema(request.__app__.name,request.get_schema())
            authorize.authorize.app_add_view(request.__app__.name, request.get_view_path())
        print "OK"