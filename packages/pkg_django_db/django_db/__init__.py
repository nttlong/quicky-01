VERSION = [1,0,0,0,0]
def get_version():
    return ".".join([x.__str__() for x in VERSION])
__db__ = None
def getdb(key = "default"):
    global __db__
    if __db__ == None:
        from pymongo import MongoClient
        from django.conf import settings
        config= settings.DATABASES[key]
        cnn = MongoClient(
            host=config["HOST"],
            port=config["PORT"]
        )
        db =cnn.get_database(config["NAME"])
        if not db.authenticate(config["USER"],config["PASSWORD"]):
            raise (Exception("Can not connect to database, auth is fail"))
        __db__ = db
    else:
        return __db__