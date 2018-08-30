from qmongo import helpers
import uuid
import threading
import bson
def generate_guid():
    return str(uuid.uuid4())