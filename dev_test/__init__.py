# import os
# import sys
# sys.path.append(os.getcwd() + os.sep + "packages")
# sys.path.append(os.getcwd() + os.sep + "packages" + os.sep + "django")
# sys.path.append(os.getcwd() + os.sep + "packages" + os.sep + "quicky")
from . import importer
importer.add_path(""
                  "")
global db_config
# import json_from_file

from quicky.db import database
db_config = json_from_file.load(os.getcwd()+os.sep+"dev_test"+os.sep+"db.json")
print(db_config)
database.connect(db_config)

