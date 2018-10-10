import django
import quicky
#import authorization
import qmongo
from performance.api import models as models_per
import quicky
from qmongo import database, helpers
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)
from HCSLS_Equipment import HCSLS_Equipment
from HCSLS_Room import HCSLS_Room
from HCSLS_TrainField import HCSLS_TrainField
from HCSLS_TrainProfession import HCSLS_TrainProfession
from performance.api.models import HCSLS_TrainSupplier
from HCSSYS_Modules import HCSSYS_Modules
from HCSSYS_FunctionListLabel import HCSSYS_FunctionListLabel
#from HCSSYS_SystemConfig import HCSSYS_SystemConfig