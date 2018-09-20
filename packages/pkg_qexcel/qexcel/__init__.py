VERSION = [1,0,"beta",1]
def get_version():
    return ".".join([x.__str__() for x in VERSION])
from . import exporters
from . repo_config import set_repo_path,get_repo_path

