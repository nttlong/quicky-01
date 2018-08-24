import os
import sys
sys.path.append(os.getcwd()+os.sep+"packages")
sys.path.append(os.getcwd()+os.sep+"packages"+os.sep+"django")
sys.path.append(os.getcwd()+os.sep+"packages"+os.sep+"quicky")
import qmongo
# fx=qmongo.helpers.expr.parse_expression_to_json_expression('start(xx.ccc.vvv,{0})','123')
reload(qmongo.helpers.expr)
qmongo.helpers.expr.parse_expression_to_json_expression("(all(ccc,{0}))",[1,2,3])
import pprint
pprint.pprint(fx)
# import config_reader
# config_reader.load("local")
# from django.contrib.auth.models import User
# users=User.objects.exists(schema="sys")
# c=User.objects.filter(username ="root", schema="sys")
# fx = c.get(schema="sys")
# print list(c)