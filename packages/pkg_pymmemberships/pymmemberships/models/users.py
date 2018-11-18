import pymqr
from pymqr import pydoc
from pymqr import pymdocs
import datetime

class Users(pymqr.pydocs):
    class ChangePasswordInfo(pymqr.pymodel.BaseModel):
        def __init__(self):
            self.OldPassword=str
            self.Time=datetime.datetime
            self.TimeUtc=datetime.datetime
    class LoginInfo(pymqr.pymodel.BaseModel):
        def __init__(self):
            self.LoginTime=datetime.datetime
            self.SessionID=str
            self.LoginTimeUTC = datetime.datetime


    def __init__(self):
        self.Username=str
        self.PasswordSalt=str
        self.HashPassword=str
        self.Emai=str
        self.PasswordChangeList=list


# model = pymqr.create_model(
users=Users()
users.set_model_name("users")
