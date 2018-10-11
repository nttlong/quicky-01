from qmongo import define
from qmongo import extends
from qmongo import extends_dict
from . commons import base_org
from . commons import base
__model_name__ = "job_works"
extends(
    __model_name__,
     base.model_name,
       [[
              "jobs.code"
       ]],
       jobs=("list",True,
              extends_dict(
                     base_org.base.base_model_info,
                     _id=("object",True),
                     is_job_w_main_staff="text",
                     report_to_job_w = ("text"),
                     internal_process = ("text"),
                     combine_process = ("text"),
                     effect_date = ("date"),
                     dept_apply =("list"),
                     dept_contact =("list"),
                     job_w_next=("list"),
                     job_w_change=("list"),
                     position_id =("object"),
                     tasks=("list",True,
                            extends_dict(
                                   base_org.base.base_model_info,
                                   _id =("object",True),
                                   weight=("numeric")
                            )
                     ),
                     appraise_factors=("list",True,
                            extends_dict(
                                   base_org.base.base_model_info,
                                   _id=("object",True),
                                   weight=("numeric")
                            )
                     ),
                     kpis =("list",True,
                            extends_dict(
                                   base_org.base.base_model_info,
                                   _id=("object",True),
                                   weight=("numeric")
                            )
                     )
              )
       )
)