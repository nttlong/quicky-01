__key__ = "__qmongo_exception_mode__"
__current_mode__ = "off"
class exept_mode():
    def __init__(self,mode):
        # if not mode in ['exception_on', 'exception_off', 'exception_return']:
        self.__old_value__= __current_mode__
        set_mode(mode)
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        set_mode(self.__old_value__)
def set_mode(mode):
    if not mode in ['on', 'off', 'return']:
        raise (Exception("'set_mode' require one text param:\n"
                         "\t on\n"
                         "\t\t Raise exception when error\n"
                         "\t off\n"
                         "\t\t Return result with error is one of the field of result. This option is default\n"
                         "\t return\n"
                         "\t\t return tuple is :(result,error)"))
    import threading
    setattr(threading.currentThread(), __key__, mode)
def get_mode():
    import threading
    if hasattr(threading.currentThread(),__key__):
        return getattr(threading.currentThread(),__key__)
    else:
        return "off"








