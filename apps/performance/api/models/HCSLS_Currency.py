from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Currency",
            "base",
            [["currency_code"]],
			currency_code=("text", True),
            currency_name=("text", True),
            currency_name2=("text"),
            temp_rate=("numeric"),
            multiply=("bool",True),
            cons_code=("text"),
            dec_place=("numeric"),
            note=("text"),
			lock=("bool"),
            ordinal=("numeric"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Currency():
    ret = db_context.collection("HCSLS_Currency")
    return ret


