from . import models
from . models import users
def create(user):
    users.users.validate(user)

