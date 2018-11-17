import pymodel
import pydoc
import pyfuncs
import pyaggregatebuilders
import pyquery
class UserInfo(pymodel.BaseEmbededDoc):
    def __init__(self):
        self.email=str
class Users(pymodel.BaseModel):
    def __init__(self):
        self.name=UserInfo()
qr=pyquery.query("employess")
qr.project(
    pydoc.document.FirstName,
    pydoc.document.LastName,
    pydoc.document.FullName<<pyfuncs.concat(pydoc.document.FirstName,' ',pydoc.document.LastName)
)
print qr.pipeline
# user=Users()
# c=pydoc.document.nam + pydoc.document.x>("1+{0}+3",15)
# print c
# pyaggregatebuilders.Match(pydoc.FilterFiels)
# c=pyaggregatebuilders.Project(
#     pydoc.document.fullName<<("concat(firstName,'{0}',lastName)","xxx")
#
# )
# print c
# c=(pyfuncs.regex(pydoc.document.name,"12"))
# print c