import re
import json
def get_field_expr(x,not_prefix=False):
    if isinstance(x,Fields):
        if x.__tree__ == None:
            if x.__name__ == None:
                return "this"
            else:
                if not not_prefix:
                    return "$"+x.__name__
                else:
                    return x.__name__
        else:
            return x.__tree__
    elif type(x) in [str,unicode]:
        import expression_parser
        return expression_parser.to_mongobd(x)
    else:
        return x

def compile(expression,*args,**kwargs):
    if isinstance(expression,Fields):
        return get_field_expr(expression)
    if type(expression) in [str,unicode]:
        import expression_parser
        return expression_parser.to_mongobd(expression,*args,**kwargs)
    if isinstance(expression,dict):
        return expression
def get_str(d,t=0):
    x=""
    for i in range(0,t,1):
       x+="\t"
    if(isinstance(d,dict)):
        ret = x+"{\n"
        for k,v in d.items():
            ret+=x+"\t"+'"'+k+'":'+get_str(v,t+1)+",\n"
        ret = ret[0:ret.__len__() - 2]
        ret += "\n\t}"
        return ret
    elif type(d) is list:
        ret=x+"[\n"
        for item in d:
            ret+=x+"\t"+get_str(item,t+1)+",\n"
        ret=ret[0:ret.__len__()-2]+x+"\n"+x+"\t"+"]"
        return ret
    elif type(d) is type(re.compile("")):
        return d.pattern
    elif type(d) in [str,unicode]:
        return '"'+d+'"'
    else:
        return d.__str__()




def __apply__(fn,a,b):
    if isinstance(b, Fields):
        ret_tree={
            fn: [get_field_expr(a), get_field_expr(b)]
        }
        setattr(a,"__tree__",ret_tree)
    elif type(b) in [str,unicode]:
        import expression_parser
        ret_tree = {
            fn: [get_field_expr (a), expression_parser.to_mongobd (b)]
        }
        setattr (a, "__tree__", ret_tree)
    elif isinstance(b,tuple) and b.__len__()>0:
        _b=b[0]
        _params=[]
        for i in range(1,b.__len__(),1):
            _params.append(b[i])
        import expression_parser
        ret_tree = {
            fn: [get_field_expr (a), expression_parser.to_mongobd (_b,*tuple(_params))]
        }
        setattr (a, "__tree__", ret_tree)
    else:
        ret_tree = {
            fn: [get_field_expr(a), b]
        }
        setattr(a, "__tree__", ret_tree)
    return a

class BaseFields(object):
    def __init__(self,data=None):
        self.__name__=None
        self.__tree__ = None
        if type(data) in [str,unicode]:
            self.__name__=data
        else:
            self.__tree__=data

class Fields(BaseFields):
    def __getattr__(self, item):
        owner = super(Fields,self)
        if item in ["__tree__","__name__","__alias__"]:
            return owner.__dict__.get(item,None)
        if hasattr(owner,"__name__"):
            return Fields(getattr(owner,"__name__")+"."+item)
        else:
            return Fields(item)
    def __setattr__(self, key, value):
        owner = super(Fields,self).__dict__
        if key in ["__tree__","__name__","__alias__"]:
            return owner.update({
                key:value
            })
        if not owner.has_key("__data__"):
            owner.update({
                "__data__":{}
            })
        owner["__data__"].update({
            key:value
        })
    def __str__(self):
        if BaseFields(self)==None:
            return "root"
        if self.__tree__==None:
            return self.__name__
        else:
            return get_str(self.__tree__)

    def __add__(self, other):
        return __apply__("$add",self,other)
    def __sub__(self, other):
        return __apply__("$subtract", self, other)
    def __mul__(self, other):
        return __apply__("$multiply", self, other)
    def __div__(self, other):
        return __apply__("$divide", self, other)
    def __mod__(self, other):
        return __apply__("$mod", self, other)
    def __eq__(self, other):
        return __apply__("$eq", self, other)
    def __ne__(self, other):
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
        return __apply__ ("$and", self, other)
    def __or__(self, other):
        return __apply__ ("$or", self, other)
    def __lshift__(self, other):
        import expression_parser
        if type(other) in [str,unicode]:
            ret =Fields()
            ret.__tree__=get_field_expr (other, True)
            ret.__dict__.update ({
                "__alias__":self.__name__
            })
            return ret
        elif isinstance(other,tuple) and other.__len__()>0:
            _other=other[0]
            _param=tuple([x for x in other if other.index(x)>0])
            ret = Fields ()
            ret.__tree__ = expression_parser.to_mongobd (_other,*_param)
            ret.__dict__.update ({
                "__alias__": self.__name__
            })
            return ret

        elif isinstance(other,Fields):
            other.__dict__.update({
                "__alias__":get_field_expr(self,True)
            })
            return other
    def __iand__(self, other):
        x= other
    def __getnewargs__(self):
        x=self
    def __rlshift__(self, other):
        x=other




    def __coerce__(self, other):
        x=other
    def __call__(self, *args, **kwargs):
        if args.__len__()==1:
            if self.__name__ != None:
                return Fields (self.__name__ + "." + args[0].__str__())
            else:
                return Fields ("this"+self.__name__ + "." + args[0].__str__())
        return  None

    def __delslice__(self, i, j):
        x=1
    def __get__(self, instance, owner):
        x = 1


document=Fields()
def fields():
    # type: () -> object
    return Fields()