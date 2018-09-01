__key__ = "__qmongo_exception_mode__"
global __stack_mode__
global __current_mode__
__current_mode__ = "off"
__stack_mode__ =[]
class except_mode():
    def __init__(self,mode):
        # if not mode in ['exception_on', 'exception_off', 'exception_return']:
        self.__mode__= mode

    def __enter__(self):
        __stack_mode__.append(get_mode())
        set_mode(self.__mode__)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if __stack_mode__.__len__()==0:
            set_mode("off")
        else:
            mode = __stack_mode__.pop()
            set_mode(mode)
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








