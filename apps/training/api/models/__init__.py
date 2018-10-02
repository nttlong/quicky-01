import django
import quicky
import authorization
import qmongo
from qmongo import database, helpers
from performance.api import models as models_per
from performance.api import models as extend
app=extend.app
db_context=extend.db_context
from HCSLS_Equipment import HCSLS_Equipment
from HCSLS_Room import HCSLS_Room
from HCSLS_TrainField import HCSLS_TrainField
from HCSLS_TrainProfession import HCSLS_TrainProfession
from performance.api.models import HCSLS_TrainSupplier
from HCSLS_TrainCourseGroup import HCSLS_TrainCourseGroup
from HCSLS_TrainLsCourse import HCSLS_TrainLsCourse
from SYS_ValueList import SYS_ValueList
from HCSLS_TrainRequest import HCSLS_TrainRequest
from HCSLS_TrainPlan import HCSLS_TrainPlan