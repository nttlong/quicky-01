import quicky
import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)
@quicky.view.template("index.html")
def index(request):
    return  request.render({})

@quicky.view.template("upload.html")
def upload(request):
    return request.render({})