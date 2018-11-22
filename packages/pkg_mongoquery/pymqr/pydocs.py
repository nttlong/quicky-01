import re
import json


def get_field_expr(x, not_prefix=False):
    if isinstance(x, Fields):
        if x.__tree__ == None:
            if x.__name__ == None:
                return "this"
            else:
                if not not_prefix:
                    return "$" + x.__name__
                else:
                    return x.__name__
        else:
            return x.__tree__
    elif type(x) in [str, unicode]:
        import expression_parser
        return expression_parser.to_mongobd(x)
    else:
        return x


def compile(expression, *args, **kwargs):
    if isinstance(expression, Fields):
        return get_field_expr(expression)
    if type(expression) in [str, unicode]:
        import expression_parser
        return expression_parser.to_mongobd(expression, *args, **kwargs)
    if isinstance(expression, dict):
        return expression


def get_str(d, t=0):
    x = ""
    for i in range(0, t, 1):
        x += "\t"
    if (isinstance(d, dict)):
        ret = x + "{\n"
        for k, v in d.items():
            ret += x + "\t" + '"' + k + '":' + get_str(v, t + 1) + ",\n"
        ret = ret[0:ret.__len__() - 2]
        ret += "\n\t}"
        return ret
    elif type(d) is list:
        ret = x + "[\n"
        for item in d:
            ret += x + "\t" + get_str(item, t + 1) + ",\n"
        ret = ret[0:ret.__len__() - 2] + x + "\n" + x + "\t" + "]"
        return ret
    elif type(d) is type(re.compile("")):
        return d.pattern
    elif type(d) in [str, unicode]:
        return '"' + d + '"'
    else:
        return d.__str__()


def __apply__(fn, a, b):
    if isinstance(b, Fields):
        ret_tree = {
            fn: [get_field_expr(a), get_field_expr(b)]
        }
        setattr(a, "__tree__", ret_tree)
    elif type(b) in [str, unicode]:
        import expression_parser
        try:
            right = expression_parser.to_mongobd(b)
        except Exception as ex:
            raise Exception("Can not apply operator +,-,*,/,.. with string constant\n"
                            "Please use pyfuncs.concat or other text function in this package")
        ret_tree = {
            fn: [get_field_expr(a), right]
        }
        setattr(a, "__tree__", ret_tree)
    elif isinstance(b, tuple) and b.__len__() > 0:
        _b = b[0]
        _params = []
        for i in range(1, b.__len__(), 1):
            _params.append(b[i])
        import expression_parser
        ret_tree = {
            fn: [get_field_expr(a), expression_parser.to_mongobd(_b, *tuple(_params))]
        }
        setattr(a, "__tree__", ret_tree)
    else:
        ret_tree = {
            fn: [get_field_expr(a), b]
        }
        setattr(a, "__tree__", ret_tree)
    return a


def __get_from_dict__(d, not_use_prefix=True):
    ret = {}
    if isinstance(d, dict):
        for k, v in d.items():
            _k = k
            if isinstance(k, Fields):
                _k = get_field_expr(k, not_use_prefix)
            ret.update({
                _k: __get_from_dict__(v, not_use_prefix)
            })
        return ret
    elif isinstance(d, Fields):
        return get_field_expr(d, not_use_prefix)
        # if d.__dict__.has_key("__alias__"):
        #     return {
        #         d.__dict__["__alias__"]:get_field_expr(d)
        #     }
        # else:
        #     return get_field_expr(d,not_use_prefix)
        # return __get_from_dict__(v,not_use_prefix)
    else:
        return d


class BaseFields(object):
    """
    Ancestor of Mongodb parsable Field
    """

    def __init__(self, data=None, for_filter=False):
        self.__name__ = None
        self.__tree__ = None
        self.__for_filter__ = for_filter
        if type(data) in [str, unicode]:
            self.__name__ = data
        else:
            self.__tree__ = data


class Fields(BaseFields):
    """
    Mongodb parable document field example:
    Fields().Amount*Fields().Price will be compile to {'$multiply': ['$Amount', '$Price']}
    """

    def __getattr__(self, item):
        if self.__name__ != None:
            return Fields(self.__name__ + "." + item, self.__for_filter__)
        else:
            return Fields(item, self.__for_filter__)

    def __str__(self):
        if BaseFields(self) == None:
            return "root"
        if self.__tree__ == None:
            return self.__name__
        else:
            return get_str(self.__tree__)

    def __add__(self, other):
        return __apply__("$add", self, other)

    def __sub__(self, other):
        return __apply__("$subtract", self, other)

    def __mul__(self, other):
        return __apply__("$multiply", self, other)

    def __div__(self, other):
        return __apply__("$divide", self, other)

    def __mod__(self, other):
        return __apply__("$mod", self, other)

    def __eq__(self, other):
        if self.__dict__.has_key("__for_filter__"):
            if type(other) in [str, unicode]:
                self.__tree__ = {
                    self.__name__: {
                        "$regex": re.compile("^" + other + "$", re.IGNORECASE)
                    }
                }
                return self
            elif self.__tree__!=None and self.__tree__!={}:
                self.__tree__ = {
                    "$eq":[self.__tree__,get_field_expr(other,True)]
                }
                return self

            else:
                self.__tree__ = {
                    self.__name__: other
                }
                return self

        return __apply__("$eq", self, other)

    def __ne__(self, other):
        if self.__for_filter:
            if type(other) in [str, unicode]:
                self.__tree__ = {
                    self.__name__:{"$ne": {
                        "$regex": re.compile("^" + other + "$", re.IGNORECASE)
                    }}
                }
                return self
            else:
                self.__tree__ = {
                    self.__name__:{"$ne": other}
                }
                return self
        return __apply__("$ne", self, other)

    def __le__(self, other):
        return __apply__("$lte", self, other)

    def __lt__(self, other):
        return __apply__("$lt", self, other)

    def __ge__(self, other):
        return __apply__("$gte", self, other)

    def __gt__(self, other):
        return __apply__("$gt", self, other)

    def __and__(self, other):
        return __apply__("$and", self, other)

    def __or__(self, other):
        return __apply__("$or", self, other)

    def __lshift__(self, other):
        import expression_parser
        if type(other) in [str, unicode]:
            ret = Fields()
            ret.__tree__ = get_field_expr(other, True)
            ret.__dict__.update({
                "__alias__": self.__name__
            })
            return ret
        elif isinstance(other, set):
            _other = list(other)
            ret_data = {}
            for item in _other:
                if isinstance(item, Fields):
                    right = get_field_expr(item, True)
                    if type(right) in [str, unicode]:
                        ret_data.update({
                            right: 1
                        })
                    elif isinstance(right, dict):
                        ret_data.update({
                            self.__name__: right
                        })

            ret = Fields()
            ret.__tree__ = ret_data
            ret.__dict__.update({
                "__alias__": self.__name__
            })
            return ret
        elif isinstance(other, tuple) and other.__len__() > 0:
            _other = other[0]
            if type(_other) in [str, unicode]:
                _param = tuple([x for x in other if other.index(x) > 0])
                ret = Fields()
                ret.__tree__ = expression_parser.to_mongobd(_other, *_param)
                ret.__dict__.update({
                    "__alias__": self.__name__
                })
                return ret
            elif isinstance(_other, Fields):
                ret_dic = {}
                for item in other:
                    ret_dic.update({
                        get_field_expr(item, True): 1
                    })
                ret = Fields()
                ret.__tree__ = ret_dic
                ret.__dict__.update({
                    "__alias__": self.__name__
                })
                return ret
        elif isinstance(other, list):
            ret_dic = []
            for item in other:
                ret_dic.append(
                    get_field_expr(item, True)
                )
            ret = Fields()
            ret.__tree__ = ret_dic
            ret.__dict__.update({
                "__alias__": self.__name__
            })
            return ret
        elif isinstance(other, Fields):
            other.__dict__.update({
                "__alias__": get_field_expr(self, True)
            })
            return other
        else:
            x = other

    def __call__(self, *args, **kwargs):
        if args.__len__() == 1:
            if self.__name__ != None:
                return Fields(self.__name__ + "." + args[0].__str__())
            else:
                return Fields("this" + self.__name__ + "." + args[0].__str__())
        return None

    def __rshift__(self, other):
        if isinstance(other, dict):
            return {
                get_field_expr(self, True): __get_from_dict__(other)
            }
        elif isinstance(other, Fields):
            return {
                get_field_expr(self, True): get_field_expr(other)
            }
        else:
            return {
                get_field_expr(self, True): other
            }
    def var(self):
        self.__name__ = "$"+self.__name__
        return self
    def asc(self):
        return {
            get_field_expr(self,True):1
        }
    def desc(self):
        return {
            get_field_expr(self, True): -1
        }
    def to_mongodb(self):
        """
        parse to mongodb expression
        :return:
        """
        if self.__dict__.has_key("__alias__"):
            if self.__tree__ == None:
                return {
                    self.__dict__["__alias__"]: self.__name__
                }
            else:
                return {
                    self.__dict__["__alias__"]: {self.__name__: self.__tree__}
                }
        if self.__tree__ == None:
            return self.__name__
        return self.__tree__


filters = Fields(None, True)
document = Fields()


def fields():
    # type: () -> object
    return Fields()


def BSON_doc(expr):
    """
        create document form field example:
        Document({
            pydoc.Fields().Name.Code:"xxx,
            pydoc.Fields().Name.Age:4
        }) =>{
            "Name.Code":"xxx",
            "Name.Age":4
        }
    :param expr:
    :return:
    """
    ret = {}
    if isinstance(expr, dict):
        for k, v in expr.items():
            if isinstance(k, Fields):
                ret.update({
                    get_field_expr(k, True): BSON_doc(v)
                })
            elif type(k) in [str, unicode]:
                ret.update({
                    k: BSON_doc(v)
                })
            else:
                raise Exception("can not convert to dict with type of key is '{0}".format(type(k)))
        return ret
    else:
        return expr


def BSON_select(*args):
    import pyquery
    pyquery.query
    ret = {}
    for item in args:
        if item.__dict__.has_key("__alias__"):
            right = __get_from_dict__(item)
            if type(right) in [str, unicode]:
                ret.update({
                    item.__dict__["__alias__"]: "$" + right
                })
            elif isinstance(right, dict):
                ret.update({
                    item.__dict__["__alias__"]: __get_from_dict__(item)
                })
            elif isinstance(right, list):
                ret.update({
                    item.__dict__["__alias__"]: right
                })
        else:
            ret.update({
                get_field_expr(item, True): 1
            })
    return ret
