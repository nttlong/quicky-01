import quicky
def authenticate(request):
    if not request.user.is_anonymous() and \
        request.user.is_active:
        return True
    else:
        return False
Database=dict(
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    name="test"
)
from qmongo import database
def db():
    from django.conf import settings
    return database.connect(
        host=settings.DATABASES["default"]['HOST'],
        port=settings.DATABASES["default"]['PORT'],
        name=settings.DATABASES["default"]['NAME'],
        user=settings.DATABASES["default"]['USER'],
        password=settings.DATABASES["default"]['PASSWORD'],
    )

Database_=dict(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms",
    tz_aware=quicky.get_django_settings_module().USE_TZ,
    timezone= "UTC"#quicky.get_django_settings_module().TIME_ZONE

)
