import pymodel
import pydoc
class UserInfo(pymodel.BaseEmbededDoc):
    def __init__(self):
        self.email=str
class Users(pymodel.BaseModel):
    def __init__(self):
        self.name=UserInfo()

x=Users()
print x.name.