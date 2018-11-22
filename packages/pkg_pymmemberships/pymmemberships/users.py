from . import models
from pymqr import documents
from pymqr import settings
from . models import users
from pymqr import query
from pymqr import funcs

class UserParam(documents.BaseDocuments):
    def __init__(self):
        self.username=str
        self.password=str
        self.email = str
userparam = UserParam()
usermodel = users.Users
def create(*args,**kwargs):
    _user=userparam.load(*args,**kwargs)
    _user_data = query(settings.getdb(),usermodel)\
        .where(funcs.regex(usermodel.Username,_user.username))\
        .find_one()
    return _user_data





