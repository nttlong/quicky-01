
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
def create(user):

    qr = query(settings.getdb(),users.Users)
    data= qr.where(users.Users.Username==user.username).object
    if data.is_empty():
        ret = qr.insert({
            users.Users.Username:user.username,
            users.Users.PasswordSalt:user.password,
            users.Users.Email:user.email,
            users.Users.Profile:{
                users.Profiles.FirstName:"test"
            }
        }).commit()

        x= data




@pyparams_validator.types(str,str)
def login(username,password):
    pass






