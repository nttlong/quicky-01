from __builtin__ import property


class __column__(object):
    def __init__(self,*args,**kwargs):

        self.caption =""
        self.field = ""
        _info = kwargs
        if type(args) is tuple and args.__len__() == 1:
            _info = args[0]
        if type(args) is tuple and args.__len__() > 1:
            _info = args
        if _info != None and type(_info) is dict:
            self.caption = _info.get("caption", "")
            self.field = _info.get("field", "")
        if _info != None and type(_info) is tuple:
            self.field = _info[0]
            if _info.__len__()>1:
                self.caption = _info[1]
class __exporter__(object):
    __columns__=[]
    def __init__(self,*args,**kwargs):
        self.__columns__ =[]
        _cols= kwargs
        if type(args) is tuple and args.__len__()>0:
            _cols = args[0]
        if type(_cols) is dict:
            for k,v in _cols.items():
                self.__columns__.append(
                    __column__(k,v)
                )
        if type(_cols) is tuple:
            for v in _cols:
                self.__columns__.append(
                    __column__(*v)
                )
    def __setattr__(self, key, *args,**kwargs):
        if key == "columns":
            _cols = kwargs
            if type(args) is tuple and args.__len__() > 0:
                _cols = args[0]
            if type(_cols) is dict:
                for k, v in _cols.items():
                    self.__columns__.append(
                        __column__(k, v)
                    )
            if type(_cols) is tuple:
                if _cols.__len__() ==0:
                    return
                else:
                    if type(_cols[0]) is tuple:
                        for v in _cols:
                            self.__columns__.append(
                                __column__(*v)
                            )
                    else:
                        self.__columns__.append(
                            __column__(_cols)
                        )
    def __getattr__(self, item):
        if item =="columns":
            return self.__columns__
        else:
            pass
    @property
    def columns(self):
        return self.__columns__











