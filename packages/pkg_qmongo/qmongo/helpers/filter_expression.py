from . import *
from . import expr
def get_param_kw(*args,**kwargs):
    if type(args) is tuple and args.__len__()>0 and type(args[0]) is dict:
        return args[0]
    if type(args) is tuple and args.__len__()>0 and not type(args[0]) is dict:
       return list(args)

class filter_expression():
    """
    this class will create a filter. From expression with parameters
    """

    def __init__(self,expression,*args,**kwargs):

        """

        :param expression:
        :param args:
        :param kwargs:
        """
        self._pipe = {}
        self._pipe = expr.parse_expression_to_json_expression(expression,*args,**kwargs)
        # params = get_param_kw(*args,**kwargs)
        # if type(params) is list:
        #     if params.__len__() ==1 and type(params[0]) is list:
        #         self._pipe = expr.parse_expression_to_json_expression(expression, params[0])
        #     else:
        #         self._pipe=expr.parse_expression_to_json_expression(expression, params)
        # else:
        #     self._pipe=expr.parse_expression_to_json_expression(expression, params)
    def And(self,expression,*args,**kwargs):
        params = get_param_kw(*args,**kwargs)
        ret=None
        if type(params) is list:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, *params)
        else:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, params)
        
        self._pipe.update({
            "$and":ret
        })
        return self
    def Or(self,expression,*args,**kwargs):
        params = get_param_kw(*args,**kwargs)
        ret=None
        if type(params) is list:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, *params)
        else:
            ret=self._pipe=expr.parse_expression_to_json_expression(expression, params)
        self._pipe.update({
            "$or": ret
        })
        return self
    def get_filter(self):
        """
        Get filter as dict for mongodb example: 
        filter('a==1')=> {"a":{"$eq":1}}
        """
        def replace_index(x):
            if type(x) is dict:
                ret = {}
                for k,v in x.items():
                    ret.update({
                        k.replace("[",".").replace("].","."):replace_index(v)
                    })
                return ret
            else:
                return x




        ret = replace_index(self._pipe)
        return ret

