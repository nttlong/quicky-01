class auth(object):
    def process_request(selfs,request):
        print request.__app__.name
        print "OK"