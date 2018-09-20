__repo_path__ = None

def set_repo_path(path):
    global __repo_path__
    __repo_path__ = path
def get_repo_path():
    global __repo_path__
    if __repo_path__ == None:
        raise Exception("It look like you forgot set repo path for qexcel")
    return __repo_path__