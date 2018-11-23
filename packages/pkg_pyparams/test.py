import pyparams
import datetime
@pyparams.types(str,str)
def login(username,password=None):
    print username,password

# @pyparams.types(dict(
#     # logins = (list,False,dict(
#     #     sessions=(list,False,dict(
#     #         x = (str,True)
#     #     ))
#     # )),
#     profiles=(dict,False,dict(
#         # first_name =(str,True),
#         # last_name = (str),
#         jobs=(list,False,dict(
#             name=(str,True),
#             info=(list,False,dict(
#                 code=(str,True)
#             ))
#         ))
#     ))
# ))
# def test(names):
#     x=1
# try:
# test(profiles = dict(
#     first_name="XXX",
#     jobs = [dict(
#         name ="xxx",
#         info = [dict(
#             code ="1234"
#         ),dict(
#             code=123
#         )]
#     )]
# ))
login("XX",123)
# except Exception  as ex:
#     x= ex