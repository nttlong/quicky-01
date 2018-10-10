from config import database, helpers, db_context
import base
import datetime
import threading
helpers.extent_model(
            "HCSSYS_SystemConfig",
            "base",
            [],
            is_has_number=("bool"),
            num_of_number=("numeric"),
            is_has_upper_char=("bool"),
            num_of_upper=("numeric"),
            is_has_lower_char=("bool"),
            num_of_lower=("numeric"),
            is_has_symbols=("bool"),
            num_of_symbol=("numeric"),

            is_ad_aut=("bool"),
            session_timeOut=("numeric"),
            time_out_expand=("numeric"),
            minimum_age=("numeric"),
            password_expiration=("numeric"),
            will_expire=("bool"),
            change_after=("numeric"),
            apply_minimum_age=("bool"),

            apply_history=("bool"),
            history=("numeric"),
            apply_minLength=("bool"),
            min_len=("numeric"),
            apply_maxLength=("bool"),
            max_len=("numeric"),
            lock_on_failed=("bool"),
            threshold_to_lock=("numeric"),
            time_lock=("numeric"),

            alert_before=("numeric"),
            is_first_change=("bool"),
            not_user_in_password=("bool"),
            date_format=("text"),
            dec_place_separator=("text"),
            dec_place_currency=("numeric"),
            default_language=("text")
        )
def HCSSYS_SystemConfig():
    ret = db_context.collection("HCSSYS_SystemConfig")
    return ret