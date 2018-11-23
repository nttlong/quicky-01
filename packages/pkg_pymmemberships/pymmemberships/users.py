
from pymqr import settings
from . models import users
from pymqr import query
from pymqr import funcs
import pyparams_validator
@pyparams_validator.types(
    username=(str,True),
    password = (str,True),
    email = (str,True)
)
def create(*args,**kwargs):
    users.Users.aggregate()
@pyparams_validator.types(str,str)
def login(username,password):
    pass






