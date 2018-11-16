import re
import json
get_field_expr=lambda x:"$"+x.__name__ if x.__tree__==None else x.__tree__
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
        ret += "\n"+x+"\t}"
        return ret
    elif type(d) is list:
        ret=x+"[\n"
        for item in d:
            ret+=x+"\t"+get_str(item,t+1)+",\n"
        ret=ret[0:ret.__len__()-2]+x+"\n"+x+"\t"+"]"
        return ret


    elif type(d) is type(re.compile("")):
        return json.dumps({
            "$regex":d.pattern
        })
    else:
        return d.__str__()





def __apply__(fn,a,b):
    if isinstance(b, Fields):
        ret_tree={
            fn: [get_field_expr(a), get_field_expr(b)]
        }
        setattr(a,"__tree__",ret_tree)
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
        if self.__name__!=None:
            return Fields(self.__name__+"."+item)
        else:
            return Fields(item)
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
    def __call__(self, *args, **kwargs):
        x=args
    def __repr__(self):
        if BaseFields(self)==None:
            return "root"
        if self.__tree__==None:
            return self.__name__
        else:
            return get_str(self.__tree__)



def fields():
    # type: () -> object
    return Fields()