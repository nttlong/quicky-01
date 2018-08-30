from config import database, helpers, db_context
helpers.define_model(
            "tmp_transactions",
            [["transaction_id"]],
            transaction_id=("text", True),
            collection_name=("text", True),
            path=("text", True),
            session=("text", True),
            ordinal=("numeric"),
            data=("text"),
            created_on=("date"),
            created_by=("text"),
        )

def tmp_transactions():
    ret = db_context.collection("tmp_transactions")
    return ret