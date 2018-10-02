import django
import quicky
#import authorization
import qmongo
from qmongo import database, helpers
from performance.api import models as models_per
from HCSLS_Equipment import HCSLS_Equipment
from HCSLS_Room import HCSLS_Room
from HCSLS_TrainField import HCSLS_TrainField
from HCSLS_TrainProfession import HCSLS_TrainProfession
from performance.api.models import HCSLS_TrainSupplier
from PortalATS.api.models import HCSSYS_Modules