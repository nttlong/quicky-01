from config import database, helpers, db_context
import base
import datetime
helpers.extent_model(
            "TMPER_AprPeriod",
            "base",
            [["apr_period", "apr_year"]],
            apr_period=("numeric", True),
			apr_year=("numeric", True),
            give_target_from=("date"),
            give_target_to=("date"),
            review_mid_from=("date"),
            review_mid_to=("date"),
			approval_mid_from=("date"),
            approval_mid_to=("date"),
            emp_final_from=("date"),
            emp_final_to=("date"),
            approval_final_from=("date"),
            approval_final_to=("date"),
            note=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMPER_AprPeriod():
    return db_context.collection("TMPER_AprPeriod")

