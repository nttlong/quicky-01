import hrm.models,datetime
from bson import ObjectId
fx=hrm.models.nations.query.update(
    {"$push":
         dict(
             provinces=dict(
                _province_id = ObjectId(),
                 code="CA",
                 name=dict(default="Cali"),
                 created_by="app",
                 created_on=datetime.datetime.now(),
                 created_on_utc=datetime.datetime.now(),
                 is_delete = False
             )
         ),

    },"code == {0}","us")