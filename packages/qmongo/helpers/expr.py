"""
Before review this document, please refer below tearm:
1- mongodb tree expression: The object that mongodb can understan see this link:https://docs.mongodb.com/manual/reference/operator/query/
2- mongodb aggregate pipeline: the list of operator in which instruct mongodb process and get data, see: https://docs.mongodb.com/manual/core/aggregation-pipeline/

"""
import _ast
import re
import inspect
from datetime import  datetime


_operators=[
    dict(op="$eq",fn=_ast.Eq),
    dict(op="$ne",fn=_ast.NotEq),
    dict(op="$gt",fn=_ast.Gt),
    dict(op="$gte",fn=_ast.GtE),
    dict(op="$lt",fn=_ast.Lt),
    dict(op="$lte",fn=_ast.LtE),
    dict(op="$multiply",fn=_ast.Mult),
    dict(op="$divide",fn=_ast.Div),
    dict(op="$mod",fn=_ast.Mod),
    dict(op="$add",fn=_ast.Add),
    dict(op="$subtract",fn=_ast.Sub),
    dict(op="$and",fn=_ast.And),
    dict(op="$or",fn=_ast.Or),
    dict(op="$not",fn=_ast.Not),
    dict(op="$in",fn=_ast.In),
    dict(op="$notin",fn=_ast.NotIn)# lis of operator will compile
    #this is  a mapping list from python operator and mongodb operator

]
_avg_funcs="sum,avg,first,last,floor,min,max,push,addToSet,meta" #aggregate function will be compile

def get_comparators(cp):
    """
    convert comparator into dict
    :param cp:
    :return:
    """
    if cp._fields.count("elts")>0:
        if type(cp.elts[0]) is _ast.Num:
            return {
                "type":"get_params",
                "index":cp.elts[0].n
            }
    if cp._fields.count("func")>0:
        fn=cp.func
        if fn.id=="get_params":
            return {
                "type": fn.id,
                "index": cp.args[0].n
            }

    raise Exception("Invalid comparators {0}".format(cp))
def get_left(cp,*params):
    """
    get left branc of expression tree
    :param cp:
    :param params:
    :return:
    """
    ret={}
    if type(cp) is _ast.Name:
        return {
            "type":"field",
            "id":cp.id
        }
    if type(cp) is _ast.Str:
        return {
            "type":"const",
            "value":cp.s
        }
    if type(cp) is _ast.Call:
        if cp.func.id=="contains":
            return {
                "function":cp.func.id,
                "params":[get_left(x,*params) for x in cp.args]
            }
        elif cp.func.id=="get_params":
            return {
                "type":"function",
                "id":"get_params",
                "value":cp.args[0].n
            }
        else:
            return {
                "type": "function",
                "id": "$"+cp.func.id,
                "params":[
                    extract_json(x, *params) for x in cp.args
                ]
            }

    if type(cp) is _ast.Set:
        return {
            "type":"const",
            "value":cp.elts[0].n
        }
    if type(cp) is _ast.Compare:
        if cp._fields.count("left")>0:
            return {
                "operator":find_operator(cp.ops[0]),
                "left":get_left(cp.left,*params),
                "right":get_right(cp.comparators[0],*params)

            }
            ret.update({
                "left":get_left(cp.left,*params)
            })
        ret.update({
            "operator":find_operator(cp.ops[0])
        })
        if cp._fields.count("comparators"):
            ret.update({
                "right": get_right(cp.comparators)
            })
    if type(cp) is _ast.BoolOp:
        return {
            "operator":find_operator(cp.op),
            "expr":[get_left(x,*params) for x in cp.values]
        }
    if type(cp) is _ast.Attribute:
        _v=cp.value
        _field=cp.attr
        while not type(_v) is _ast.Name:
            if type(_v) is _ast.Attribute:
                _field=_v.attr+"."+_field

            if type(_v) is _ast.Subscript:
                if type(_v.slice) is _ast.Index:
                    if type(_v.slice.value) is _ast.Call and _v.slice.value.func.id=="get_params":
                        _field = "[" + _v.slice.value.args[0].n.__str__() + "]." + _field
                    else:
                        _field = "[" + _v.slice.value.n.__str__() + "]." + _field
                # if type(_v.slice) is _ast.Index:
                #     _field = "[" + _v.slice.value.n.__str__() + "]." + _field


            _v = _v.value

        _field=_v.id+"."+_field
        return _field.replace(".[","[")






        if cp.value._fields.count("slice")>0:
            return cp.value.value.id + "["+cp.value.slice.value.n.__str__()+"]." + cp.attr
        else:
            return cp.value.id + "." + cp.attr
    if type(cp) is _ast.Num:
        return {
            "type":"const",
            "value":cp.n
        }




    return ret;
def get_right(cp,*params):
    """
    Get right brance of expression tree
    :param cp:
    :param params:
    :return:
    """
    if type(cp) is list:
        return "_"
    ret={}
    if type(cp) is list:
        if cp.__len__()>1 and\
            type(cp[0]) is _ast.Call and\
            type(cp[1]) is _ast.Num:
            return {
                "type":"function",
                "id":cp[0].func.id,
                "params":[cp[1].n]
            }
        if cp.__len__()==1 and\
            type(cp[0]) is _ast.Call and\
            cp[0].func.id=="get_params" and \
            type(cp[0].args[0]) is _ast.Num :
            return {
                "type":"params",
                "value":cp[0].args[0].n
            }
        if cp.__len__()==1 and type(cp[0]) is _ast.Str:
            return {
                "type":"const",
                "value":cp[0].s
            }



        if type(cp[0]) is _ast.Num:
            return {
                "type": "const",
                "value":cp[0].n
            }
    if type(cp) is _ast.Num:
        return {
            "type":"const",
            "value":cp.n
        }
    if type(cp) is _ast.List:
        return {
            "type":"const",
            "value":[x.n for x in cp.__reduce__()[2]['elts']]
        }

    if type(cp) is _ast.Str:
        return {
            "type":"const",
            "value":cp.s,
            "data_type":"string"
        }

    if type(cp) is _ast.Compare:
        return {
            "left":get_left(cp.left,*params),
            "operator":find_operator(cp.ops[0]),
            "right":get_right(cp.comparators[0],*params)
        }
    if type(cp) is list and\
            cp.__len__()==1 and \
            cp[0]._fields.count("func")>0 and \
            cp[0].func.id=="contains":

        return {
            "type":"function",
            "id":cp[0].func.id,
            "field":cp[0].args[0].s,
            "value":cp[0].args[1].s
        }
    if type(cp) is list and cp.__len__()==1 and \
        type(cp[0]) is _ast.Set and \
        cp[0]._fields.count('elts') > 0:
        return {
            "type":"const",
            "value":cp[0].elts[0].n
        }
    if cp._fields.count("ops")>0:
        ret.update({
            "operator": find_operator(cp.ops[0])
        })
        if cp._fields.count("left")>0:
            ret.update({
                "left": get_left(cp.left,*params)
            })
        if cp._fields.count("comparators"):
            ret.update({
                "left": get_left(cp.comparators[0],*params)
            })
        if cp._fields.count("values")>0:
            ret.update({
                "right": get_right(cp.value.values[1],*params)
            })
    if type(cp) is _ast.Call and cp.func.id.lower()=="contains":
        if cp.args[1]._fields.count("s")>0:
            return {
                "type":"function",
                "id":"contains",
                "field":cp.args[1].s
            }
        if cp.args[1]._fields.count("elts")>0:
            return {
                "type": "function",
                "id": "contains",
                "field": cp.args[1].s
            }
    if type(cp) is _ast.Call and cp.func.id.lower() == "get_params":
        return {
            "type":"params",
            "value":cp.args[0].n
        }
    if type(cp) is _ast.Name:
        return  get_left(cp,params)






    return ret
def find_operator(op):
    """
    Find is python operator in map at _operators on the top this file
    :param op:
    :return:
    """
    for x in _operators:
        if type(op) is x["fn"]:
            return x["op"]
    raise Exception("Invalid comparators {0}".format(op))
def vert_expr(str,*params):
    """
    Parameterize expression
    :param str:
    :param params:
    :return:
    """
    ret=str
    index=0
    for p in params:
        ret=ret.replace("{"+index.__str__()+"}","get_params("+index.__str__()+")")
        index=index+1
    return ret
def get_tree(expr,*params,**kwargs):
    """
    get full tree of expression
    :param expr:
    :param params:
    :param kwargs:
    :return:dict of tree expression including {op:<operator>, left:<left branch>, right:<right branch>}
    """
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        params=params[0]
    if type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        _params=[]
        _expr=expr
        _index=0;
        for key in params[0].keys():
            _expr=_expr.replace("@"+key,"{"+_index.__str__()+"}")
            _params.append(params[0][key])
            _index+=1
        expr=_expr
        params=_params
    elif type(params) is dict:
        _params = []
        _expr = expr
        _index = 0;
        for key in params.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(params[key])
            _index += 1
        expr = _expr
        params = _params
    elif params==():
        _params = []
        _expr = expr
        _index = 0;
        for key in kwargs.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(kwargs[key])
            _index += 1
        expr = _expr
        params = _params


    ret={}
    if expr[0:5]=="expr(":
        return get_calc_expr(expr,*params,**kwargs)

    str=vert_expr(expr,*params)
    cmp=compile(str, '<unknown>', 'exec', 1024).body.pop()
    if type(cmp.value) is _ast.UnaryOp:
        if type(cmp.value.operand) is _ast.Call:
            if cmp.value.operand.func.id == "all":
                return {
                    "operator": find_operator(cmp.value.op),
                    "left": get_left(cmp.value.operand.args[0],*params)['id'],
                    "right": get_func_all(cmp.value.operand,*params)

                }
            if cmp.value.operand.func.id == "elemMatch":
                return {
                    "operator": find_operator(cmp.value.op),
                    "left": get_left(cmp.value.operand.args[0], *params)['id'],
                    "right": get_elem_match(cmp.value.operand, *params)

                }
            if cmp.value.operand.func.id in ["contains","start","end"]:
                return {
                    "operator": find_operator(cmp.value.op),
                    "left": get_left(cmp.value.operand.args[0], *params)['id'],
                    "right": get_mongo_text_function(cmp.value.operand,cmp.value.operand.func.id,*params)

                }


        return {
            "operator":find_operator(cmp.value.op),
            "left":get_left(cmp.value.operand.left,*params),
            "right":get_right(cmp.value.operand,*params)


        }

    if type(cmp.value) is _ast.BoolOp:
        return {
            "operator": find_operator(cmp.value.op),
            "left": [get_left(x, *params) for x in cmp.value.values],
            "right": None
        }
    if type(cmp.value) is _ast.Compare:
        return {
            "left":get_left(cmp.value.left,*params),
            "operator":find_operator(cmp.value.ops[0]),
            "right":get_right(cmp.value.comparators[0],*params)
        }

    if cmp.value._fields.count("left")>0:
        ret.update({
            "left":get_left(cmp.value.left,*params)
        })
    if cmp.value._fields.count("right")>0:
        ret.update({
            "right":{
                "id":cmp.value.right.id,
                "type":"field"
            }
        })
    elif cmp.value._fields.count("comparators")>0:
        ret.update({
            "right": get_comparators(cmp.value.comparators[0])
        })
    if cmp.value._fields.count("ops")>0:
        ret.update({
            "operator": find_operator(cmp.value.ops[0])
        })
    if cmp.value._fields.count("op")>0:
        if type(cmp.value.values[1]) is _ast.Call:
            return {
                "operator": find_operator(cmp.value.op),
                "left": get_left(cmp.value.values[0], *params),
                "right": get_left(cmp.value.values[1], *params)
            }
        else:
            return {
                "operator": find_operator(cmp.value.op),
                "left": get_left(cmp.value.values[0], *params),
                "right": get_right(cmp.value.values[1], *params)
            }
    if type(cmp.value) is _ast.BoolOp:
        return {
            "operator":find_operator(cmp.value.op),
            "left":get_left(cmp.value.values[0],*params),
            "right": get_left(cmp.value.values[1],*params)
        }
    if type(cmp.value) is _ast.Call:
        if cmp.value.func.id in ["contains","start","end"]:
            return get_mongo_text_function(cmp,cmp.value.func.id,*params)
        elif cmp.value.func.id=="notContains":

            fx = get_left(cmp.value, *params)
            if fx['params'].__len__() < 2:
                raise Exception("notContains function must have one text param")
            val = get_str_value_of_text_function(cmp, params)
            if not type(val) in [type(str), type(unicode)]:
                raise Exception("notContains function is expected one text param, but the value {0} is not a text".format(val))
            return {
                "left": fx['params'][0],
                "operator": "$notContains",
                "right": fx['params'][1]
            }

        elif cmp.value.func.id == "exists":
            fx= get_left(cmp.value)
            return {
                "left":fx['params'][0],
                "operator":"$exists",
                "right":True
            }

        elif cmp.value.func.id == "notExists":
            fx = get_left(cmp.value)
            return {
                "left": fx['params'][0],
                "operator": "$exists",
                "right": False
            }
        elif cmp.value.func.id == "_in":
            fx = get_left(cmp.value,*params)
            if fx['params'].__len__() <2:
                raise (Exception("_in must have one list params"))
            _params = fx["params"][1]
            if _params == None:
                if not type(cmp.value.args[1]) is list:
                    raise (Exception("_in must have one list params,but unexpected type"))
                _params =[x.n for x in cmp.value.args[1].__reduce__()[2]['elts']]
            return {
                "left": fx['params'][0],
                "operator": "$in",
                "right": _params
            }
        elif cmp.value.func.id == "not_in":
            fx = get_left(cmp.value, *params)
            if fx['params'].__len__() <2:
                raise (Exception("not_in must have one list params"))
            _params = fx["params"][1]
            if _params == None:
                if not type(cmp.value.args[1]) is list:
                    raise (Exception("not_in must have one list params,but unexpected type"))
                _params =[x.n for x in cmp.value.args[1].__reduce__()[2]['elts']]
            return {
                "left": fx['params'][0],
                "operator": "$nin",
                "right": _params
            }
        elif cmp.value.func.id in ["_all","all"]:
            return get_func_all(cmp,*params)
        elif cmp.value.func.id == "_not":
            fx = get_left(cmp.value, *params)
            if fx['params'].__len__() <2:
                raise (Exception("_not must have one object params"))
            _params = fx["params"][1]
            if _params == None:
                if not type(cmp.value.args[1]) is list:
                    raise (Exception("_all must have one list params,but unexpected type"))
                _params =[x.n for x in cmp.value.args[1].__reduce__()[2]['elts']]
            return {
                "left": fx['params'][0],
                "operator": "$not",
                "right": _params
            }
        elif cmp.value.func.id =="elemMatch":
            return get_elem_match(cmp, params)
        elif cmp.value.func.id in ["nor","_and","_or"]:
            args = [get_right(x, *params) for x in cmp.value.args]
            return {
                "operator":cmp.value.func.id,
                "right":args
            }
        elif cmp.value.func.id == 'isType':
            fy = get_right(cmp.value.args[1],*params)
            if fy['type']=='const':
                if not type(fy['value']) in [type(str),type(unicode)]:
                    raise (Exception("The second param of 'isType' must be text, but the value is {0}\n"
                                     "Detail:\n"
                                     "{1}".format(fy['value'],expr)))
                return {
                    "left": get_left(cmp.value.args[0]),
                    "operator": "isType",
                    "right":fy['value']

                }
            if fy['type'] == 'params':
                val = params[fy['value']]
                if not type(val) in [type(str),type(unicode)]:
                    raise (Exception("The second param of 'isType' must be text, but the value is {0}\n"
                                     "Detail:\n"
                                     "{1}".format(val,expr)))
                return {
                    "left": get_left(cmp.value.args[0]),
                    "operator": "isType",
                    "right": val

                }
        elif cmp.value.func.id == "search":
            fx = get_right(cmp.value.args[0],*params)
            if fx['type'] =='const':
                return {
                    "left": "$text",
                    "operator": "$search",
                    "right": fx['value']
                }
            else:
                return {
                    "left": "$text",
                    "operator": "$search",
                    "right":params[fx['value']]
                }

            val = get_str_value_of_text_function(cmp, params)
            return {
                "left": "text",
                "operator": "$search",
                "right": val
            }

        else:
            support_funcs="contains(field name,text value)\n" \
                          "notContains(field name,text value)" \
                          "start(field name,text value)\n" \
                          "end(field name,text value)\n" \
                          "exists(field name)\n" \
                          "notExists(fiel name)," \
                          "_in(field name, array)\n" \
                          "not_in(field name, array)," \
                          "_all(field name, array)\n" \
                          "elemMatch(conditional)\n" \
                          "_and(logical expr 1,..,logical expr n)\n" \
                          "_or(logical expr 1,..,logical expr n)\n" \
                          "isType(field name,the text describe mongodb type)\n" \
                          "expr(logic expression)\n" \
                          "search(text search value)" \
                          "nor(logical expr 1,..,logical expr n)\n ------------  '\_(^|^)_/`------------"



            raise (Exception("unknown function '{0}'. Validate function in match are bellow:\n{1}".format(cmp.value.func.id,support_funcs)))





    return ret


def get_mongo_text_function(cmp,fn_name,*params):
    if type(cmp) is _ast.Call:
        fx = get_left(cmp.args[0], *params)
        fy = get_right(cmp.args[1], *params)
        if fx['type'] == 'params':
            return {
                fx['id']: {
                    "operator": "${0}".format(fn_name),
                    "right":params[fy["value"]]
                }
            }
        else:
            return {
                fx['id']: {
                    "operator": "${0}".format(fn_name),
                    "right": fy["value"]
                }
            }

        return {
            fx['id']:{
                "operator":"${0}".format(fn_name),

            }
        }

    fx = get_left(cmp.value, *params)
    if fx['params'].__len__() < 2:
        raise Exception("{0}  function must have one text param".format(fn_name))
    val = get_str_value_of_text_function(cmp, params)
    if not type(val) in [str, unicode]:
        raise Exception("{1} function is expected one text param, but the value {0} is not a text".format(val,fn_name))
    return {
        "left": get_expr(fx['params'][0]),
        "operator": "${0}".format(fn_name),
        "right": val
    }



def get_func_all(cmp,*params):
    if type(cmp) is _ast.Expr:
        args = cmp.value.args
    else:
        args = cmp.args
    if args.__len__() != 2:
        raise (Exception("all need two params\n The first is a field name and the second is list of items"))
    fx = get_right(args[1],*params)
    _params = None
    if fx['type'] == "const":
        _params = fx["value"]
    elif fx['type'] == 'params':
        _params =params[fx['value']]
    else:
        _params =get_left(cmp.value,*params)['params'][1]
    if _params == None:
        if not type(args[1]) is list:
            raise (Exception("_all must have one list params,but unexpected type"))

    return {
        "left": get_left(args[0], *params)['id'],
        "operator": "$all",
        "right": _params
    }



def get_elem_match(cmp, *params):
    args =[]
    if type(cmp) is _ast.Call:
        args =cmp.args
    if type(cmp) is _ast.Expr:
        args =cmp.value.args

    _left = get_left(args[0])
    if args.__len__() > 2:
        if type(_left) is dict:
            _left = _left["id"]

        return {
            "left": _left,
            "operator": "$elemMatch",
            "right": [get_left(x) for x in args if args.index(x) > 0]

        }
    else:
        if type(_left) is dict:
            _left = _left["id"]

        return {
            "left": _left,
            "operator": "$elemMatch",
            "right": get_left(args[1], *params)

        }


def get_str_value_of_text_function(cmp, params):
    if type(cmp.value.args[1]) is _ast.Call and cmp.value.args[1].func.id == "get_params":
        val = params[cmp.value.args[1].args[0].n]
    else:
        val = cmp.value.args[1].__reduce__()[2]['s']
    return val

__compile_right_params__ = lambda x,y: x[y["right"]["value"]] if y.get('right',{}).get('type',None) == "params" else y["right"]["value"]
def raw_string(s):
    if not type(s) in [str,unicode]:
        return s
    if s == '':
        return s
    for c in ['$','^','?','*']:
        s = s.replace(c,'\\'+c)
    s=s.replace('/','\/')
    if isinstance(s, str):
        if s[s.__len__()-1] in ['\\','/8']:
            s=s[0:s.__len__()-1]+ s[s.__len__()-1].encode('string-escape')
    elif isinstance(s, unicode):
        if s[s.__len__() - 1] == '\\':
            s = s[0:s.__len__() - 1] + s[s.__len__() - 1].encode('unicode-escape')
    return s

def get_expr(fx,*params):
    """
    Convert tree of expression into mongodb aggregate pipe
    :param fx:
    :param params:
    :return:
    """
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is tuple:
        params=params[0]
    while type(params) is tuple and params.__len__()>0 and type(params[0]) is dict:
        params = params[0]
    if type(params) is dict:
        params=[params[key] for key in params.keys()]

    if(type(fx) in [str,unicode]):
        return fx
    ret={}
    if fx.has_key('operator'):
        if fx['operator'] in ['nor',"_and","_or"]:
            get_value_of_param = lambda x,y: x if y==() else y[x]
            return {
                '$'+fx['operator'].replace('_',''):[get_expr(x,*params) for x in fx['right']]
            }
        if fx["operator"] =="$elemMatch":
            if type(fx['right']) is list:
                _right = {}
                for x in fx['right']:
                    _x =get_expr(x)
                    _right.update(_x[_x.keys()[0]])
                return {
                    fx['left']: {
                        '$elemMatch': _right
                    }
                }

            if fx['right'].has_key('expr'):
                return {
                    fx['left']:{
                        '$elemMatch':{
                            fx['right']['operator']:[get_expr(x,*params) for x in fx["right"]['expr']]
                        }
                    }
                }
            else:
                return {
                    fx['left']: {
                        '$elemMatch': get_expr(fx['right'])
                    }
                }

        if fx["operator"] == "$notin":

            return {
                get_expr(fx["left"]):{
                    "$ne":{
                        "$in":__compile_right_params__(params,fx)
                    }
                }
            }

        if fx["operator"] == "$in":
            return {
                get_expr(fx["left"]): {
                    fx["operator"]: __compile_right_params__(params, fx)
                }
            }

        if fx["operator"] == "$not":
            if fx['right'][fx['right'].keys()[0]]['operator'] in ["$contains",'$start','$end']:
                cx = get_expr(dict(operator='contains', right='ccc', left='dddd'))
                cx = get_expr(
                    dict(
                        operator=fx['right'][fx['right'].keys()[0]]['operator'],
                        right=(lambda x,y: y if x==() else x[y])(params,fx['right'][fx['right'].keys()[0]]['right']),
                        left=fx['right'].keys()[0])
                )
                cx[cx.keys()[0]] = {"$not": cx[cx.keys()[0]]}
                return cx

            _right_expr = get_expr(fx['right'],params)
            if _right_expr.keys()[0] == "$all":
                _r =get_expr(fx['right'],params)
                return {
                    fx['right']['params'][0]:{
                        "$not":{
                            "$all":fx['right']['params'][1]
                        }
                    }
                }

            if _right_expr[_right_expr.keys()[0]].keys()[0] == "$in":
                return {
                    _right_expr.keys()[0]:{
                        "$nin":_right_expr[_right_expr.keys()[0]][_right_expr[_right_expr.keys()[0]].keys()[0]]
                    }
                }
            if _right_expr[_right_expr.keys()[0]].keys()[0] == "$elemMatch":
                return {
                    _right_expr.keys()[0]:{
                        "$not": {
                            "$elemMatch": _right_expr[_right_expr.keys()[0]][_right_expr[_right_expr.keys()[0]].keys()[0]]
                        }
                    }
                }


            return {
                fx["left"]:{
                    fx["operator"]:get_expr(fx['right'],params)
                }
            }

        if fx.has_key("type") and fx["type"]=="const":
            return fx["value"]
        if fx.has_key("type") and fx["type"]=="field":
            return fx["id"]
        if fx["operator"] == "isType":
            return {
                fx['left']:{
                    '$type':fx['right']
                }

            }

        if fx["operator"]=="$contains":
            return {
                fx["left"]:re.compile(raw_string(fx["right"]),re.IGNORECASE)

            }
        if fx["operator"]=="$start":
            return {
                fx["left"]:re.compile(r"^"+raw_string(fx["right"]),re.IGNORECASE)

            }
        if fx["operator"]=="$end":
            return {
                fx["left"]:re.compile(raw_string(fx["right"])+r"$",re.IGNORECASE)

            }
        if fx["operator"]=="$notContains":
            return {
                fx["left"]:re.compile(r"^(?!.*?"+raw_string(fx["right"])+r").*$" ,re.IGNORECASE)

            }
        if fx["operator"]=="$eq":
            if type(fx["right"]) in [str,unicode]:
                if fx["left"].has_key("type")and fx["left"]["type"]=="field":
                    return {
                        fx["left"]["id"]: {
                            "$regex": re.compile(raw_string(fx["right"]), re.IGNORECASE)
                        }
                    }
                else:
                    return {
                        fx["left"]: {
                            "$regex": re.compile(raw_string(fx["right"]), re.IGNORECASE)
                        }
                    }
            else:
                if fx["right"]["type"]=="params":
                    val=params[fx["right"]["value"]]
                    if type(val) in [str,unicode]:
                        if type(fx["left"]) in [str,unicode]:
                            return {
                                fx["left"]: {
                                    "$regex": re.compile("^" + raw_string(val) + "$", re.IGNORECASE)
                                }
                            }
                        else:
                            return {
                                fx["left"]["id"]:{
                                    "$regex":re.compile("^"+raw_string(val)+"$",re.IGNORECASE)
                                }
                            }
                    else:
                        if fx["operator"]=="$eq" and type(val) in [str,unicode]:
                            if type(fx["left"]) in [str,unicode]:
                                return {
                                    fx["left"]: {
                                        "$regex":re.compile("^"+raw_string(val)+"$",re.IGNORECASE)
                                    }

                                }
                            if type(fx["left"]) is dict:
                                return {
                                    fx["left"]["id"]:{
                                        "$regex":re.compile("^"+raw_string(val)+"$",re.IGNORECASE)
                                    }

                                }

                        else:
                            if type(fx["left"]) in [str,unicode]:
                                return {
                                    fx["left"]:{
                                        fx["operator"]: val
                                    }

                                }
                            if type(fx["left"]) is dict:
                                return {
                                    fx["left"]["id"]: {
                                        fx["operator"]: val
                                    }

                                }

                if fx["right"]["type"]=="const":
                    val = fx["right"]["value"]
                    if type(val) in [str,unicode]:
                        if type(fx["left"]) in [str,unicode]:
                            return {
                                fx["left"]: {
                                    "$regex": re.compile("^" + raw_string(val) + "$", re.IGNORECASE)
                                }
                            }
                        return {
                            fx["left"]["id"]: {
                                "$regex": re.compile("^" + raw_string(val) + "$", re.IGNORECASE)
                            }
                        }
                    else:
                        if fx["left"]=={}:
                            return val
                        elif type(fx["left"]) in [str,unicode]:
                            return {
                                fx["left"]: {
                                    fx["operator"]: val
                                }
                            }
                        elif fx["left"].has_key("id"):
                            return {
                                fx["left"]["id"]: {
                                    fx["operator"]: val
                                }
                            }
        else:
            if fx.has_key("right"):
                if fx["right"]!=None:
                    if not type(fx["right"]) is dict:
                        return {
                            get_expr(fx["left"], *params): {
                                fx["operator"]: fx["right"]
                            }
                        }
                    else:
                        if fx["right"].get("type","") == "const":
                            val = fx["right"]["value"]
                            if fx["left"]=={}:
                                return val
                            else:
                                return {
                                    get_expr(fx["left"], *params):{
                                        fx["operator"]:val
                                    }
                                }

                        if fx["right"].get("type","") == "params":
                            val =params[fx["right"]["value"]]
                            if type(fx["left"]) is dict and fx["left"]["type"]=="field":
                                val=fx["right"]["value"]
                                if fx["right"]["type"]=="params":
                                    val=params[val]
                                # if fx["right"]["type"]=="function" and fx["right"]["id"]=="get_params":

                                return {
                                    fx["left"]["id"]: {
                                        fx["operator"]: val
                                    }
                                }
                            else:
                                return {
                                    fx["left"]: {
                                        fx["operator"]: val
                                    }
                                }
                        if fx["right"].get("function","") == "contains":
                            if fx.has_key("params"):
                               if fx["params"][1].get("type","")=="const":
                                    return {
                                        fx["params"][0]["id"]:fx["params"][1]["value"]
                                    }
                               if fx["params"][1].get("type", "") == "params":
                                   return {
                                       fx["params"][0]["id"]:params[fx["params"][1]["value"]]
                                   }
                            if fx.has_key("operator"):
                                return {
                                    fx["operator"]:[
                                        get_expr(fx["left"],*params),
                                        get_expr(fx["right"], *params)
                                    ]
                                }
                elif type(fx["left"]) is list:
                    ret_json={
                        fx["operator"]:[]
                    }
                    for item in fx["left"]:
                        _m=get_expr(item,*params)
                        ret_json[fx["operator"]].append(_m)
                    return ret_json
            if fx.has_key("operator") and fx.has_key("expr"):
                ret_json={
                    fx["operator"]:[]
                }
                for item in fx["expr"]:
                    _m=get_expr(item,*params)
                    ret_json[fx["operator"]].append(_m)
                return ret_json
                # return {
                #     fx["operator"]:[
                #         get_expr(x,*params) for x in fx["expr"]
                #     ]
                # }
    elif fx.has_key("type"):
        if fx["type"]=="function":
            return {
                fx["id"]: [fx["params"]]
            }
        elif fx["type"] == "field":
            return fx["id"]

    elif fx.has_key("function") and fx["function"].lower()=="contains":
        if fx["params"][1].has_key("value"):
            if fx["params"][1].has_key("type") and\
               fx["params"][1]["type"]=="function" and\
                fx["params"][1]["id"]=="get_params":
                return {
                    fx["params"][0]["id"]:{"$regex":re.compile(raw_string(params[fx["params"][1]["value"]]),re.IGNORECASE)}
                }
            else:
                return {
                    fx["params"][0]["id"]:{"$regex":re.compile(raw_string(fx["params"][1]["value"]),re.IGNORECASE)}
                }
    else:
        return {
            fx["operator"]:[
                get_expr(fx["left"],*params),
                get_expr(fx["right"],*params)
            ]
        };


def get_calc_exprt_boolean_expression(fx,*params):
    """
    Convert python tree expression into mongodb filter expression
    :param fx:
    :param params:
    :return:
    """
    _get_val_ = lambda x,y:x if y ==() else y[x]

    if type(fx) is _ast.Num:
        return _get_val_(fx.n,params)

    p=get_right(fx,*params)
    if fx._fields.count("left")>0 and type(fx.left) is _ast.Call:
        field = get_left(fx.left.args[0])
        if p["right"]["type"]=="const":
            return {
                p["operator"]:[
                    {
                        "$" + fx.left.func.id:"$"+field["id"]
                    },p["right"]["value"]
                ]
            }
        if p["right"]["type"]=="params":
            return {
                p["operator"]: [
                    {
                        "$" + fx.left.func.id: "$" + (lambda x: x if type(x) in [str,unicode] else x["id"])(field)
                    }, params[p["right"]["value"]]
                ]
            }
    if type(fx) is _ast.Compare:
        return {
            find_operator(fx.ops[0]):[
                get_calc_exprt_boolean_expression(fx.left,*params),
                get_calc_exprt_boolean_expression(fx.comparators[0],*params)
            ]
        }
    if type(fx) is _ast.BoolOp:
        return {
            find_operator(fx.op): [
                [get_calc_exprt_boolean_expression(x,*params) for x in fx.values]

            ]
        }
    if type(fx) is _ast.Name:
        return get_left(fx,*params)
def extract_json(fx,*params):
    """
    Convert pythong tree expression into mongodb selector in $project of mongodb aggregate
    :param fx:
    :param params:
    :return:
    """
    if type(fx) is _ast.BoolOp:
        return {
            find_operator(fx.op):[  extract_json(x, *params)  for x in fx.values ]
        }
    if type(fx) is _ast.Attribute:
        return "$"+get_left(fx)
    if type(fx) is _ast.Name:
        p=get_left(fx,*params)
        return "$"+p["id"]
    if type(fx) is _ast.Num:
        return fx.n
    if type(fx) is _ast.Str:
        return fx.s

    if type(fx) is _ast.Call:
        if fx.func.id=="expr":
            return {
                "$expr":extract_json(fx.args[0],*params)
            }

        if fx.func.id=="get_params":
            return params[fx.args[0].n]

        if fx.func.id=="iif":
            return {
                "$cond": { "if": get_calc_exprt_boolean_expression(fx.args[0],*params),
                           "then": extract_json(fx.args[1],*params),
                            "else": extract_json(fx.args[2],*params) }
            }
        if  _avg_funcs.find(fx.func.id)>-1:
            return {
                "$"+fx.func.id:extract_json(fx.args[0])
            }
        elif fx.func.id=="dateToString":
            p_left = get_left(fx.args[0],*params)
            p_right = get_left(fx.args[1],*params)
            val=p_right["value"]
            if p_right["type"]=="function" and p_right["id"]=="get_params":
                val=params[val]
            # return { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
            return {
                "$dateToString":{
                    "format":val,
                    "date":"$"+p_left["id"]

                }
            }
        elif fx.func.id=="dateFromString":
            p_left = get_left(fx.args[0], *params)
            p_right = get_left(fx.args[1], *params)
            val = p_right["value"]
            if p_right["type"] == "function" and p_right["id"] == "get_params":
                val = params[val]
            # return { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
            return {
                "$dateToString": {
                    "timezone": val,
                    "dateString": "$" + p_left["id"]

                }
            }
        elif fx.func.id=="switch":
            branches=[]
            for item in fx.args:
                if fx.args.index(item)<fx.args.__len__()-1:

                    branches.append({
                        "case":extract_json(item.args[0],*params),
                        "then":extract_json(item.args[1],*params)

                    })

            return {
                "$switch":{
                    "branches":branches,
                    "default":extract_json(fx.args[fx.args.__len__()-1],*params)
                }
            }
            k=cmp
            pass

        else:
            return {
                "$"+fx.func.id:[
                    extract_json(x,*params) for x in fx.args

                ]
            }
    if type(fx) is _ast.BinOp:
        return {
            find_operator(fx.op):[
                extract_json(fx.left,*params),
                extract_json(fx.right,*params)
            ]
        }
    if type(fx) is _ast.Compare:
        return {
            find_operator(fx.ops[0]):[
                extract_json(fx.left, *params),
                extract_json(fx.comparators[0], *params)
            ]

        }
def get_calc_expr_boolean_expression_result(fx,*params):
    """Apply parameters in expression to real value
    Why this is important?
    the fx parameter is a dict of tree expression include operator, left and right but the right brance maybe contains parameter
    This function will fetch parameters in to fx
    """
    p = get_left(fx,*params)
    if p["type"]=="const":
        return p["value"]
    if p["type"]=="function" and p["id"]=="get_params":
        return params[p["value"]]
def get_calc_expr(expr,*params,**kwargs):
    # type: (str,bool) -> dict
    # type: (str,str) -> dict
    # type: (str,unicode) -> dict
    # type: (str,datetime) -> dict
    # type: (str,list) -> dict
    # type: (str,tuple) -> dict
    # type: (str,dict) -> dict
    """
    Conver text expression with parameters into mongodb json expression
    :param expr:
    :param params:
    :param kwargs:
    :return:mongodb json experession
    """
    if expr==1:
        return expr
    if type(params) is tuple and params.__len__() > 0 and type(params[0]) is dict:
        _params = []
        _expr = expr
        _index = 0
        for key in params[0].keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(params[0][key])
            _index += 1
        expr = _expr
        params = _params
    elif params == ():
        _params = []
        _expr = expr
        _index = 0;
        for key in kwargs.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(kwargs[key])
            _index += 1
        expr = _expr
        params = _params
    if callable(expr):
        field_name=inspect.getsource(expr).split('=')[0]
        expr=inspect.getsource(expr)[field_name.__len__()+1:inspect.getsource(expr).__len__()]


    expr=vert_expr(expr,*params)
    cmp = None
    try:
        cmp = compile(expr, '<unknown>', 'exec', 1024).body.pop()
    except Exception as ex:
        import sys, traceback
        raise (Exception("'{0}' is invalid expression\n details:\n {1}".format(expr,traceback.print_exc(file=sys.stdout))))
    return extract_json(cmp.value,*params)
def get_calc_get_param(fx,*params):
    """
    Convert python tree expression into mongodb tree expression
    :param fx:
    :param params:
    :return:
    """
    if type(fx) is _ast.Name:
        return "$"+get_calc_get_names(fx)
    if type(fx) is _ast.Str:
        return fx.s

    if type(fx) is _ast.Num:
        return fx.n
    if type(fx) is _ast.Attribute:
        return "$" + get_left(fx)
def get_calc_get_names(fx):
    return fx.id
def verify_match(fx):
    """
    Check is fx a logical expresion
    :param fx:
    :return:
    """
    if fx=={}:
        return "The left side of the expression is not a field of the document. " \
               "It look like your expression is not a logical expression"
    if not fx.has_key("left"):
        return None
    if fx["left"].has_key("type") and fx["left"]["type"] == "function":
        return "The left side of the expression is not a field of the document. " \
               "It look like you use function. function name is '{0}' ".format(fx["left"]["id"])

    if type(fx["left"]) is list:
        index=0
        msg=None
        while msg==None and index<fx["left"].__len__():
            msg = verify_match(fx["left"][index])
            index=index+1
        return msg


    if fx["left"].has_key("type") and  fx["left"]["type"] =="const":
        return "The left side of the expression is not a field of the document. " \
               "It look like constant or expression. Actually expression is '{0}'  "\
            .format(fx["left"]["value"])
    else:
        return verify_match(fx["left"])
def parse_expression_to_json_expression(expression,*params,**kwargs):
    import sys, traceback

    """
    Convert text expression into mongodb tree expression
    :param expression:
    :param params:
    :param kwargs:
    :return:
    """
    try:
        expr_tree=get_tree(expression,*params,**kwargs)
        if expression[0:5]=="expr(":
            return expr_tree
        if params.__len__()>0:
            params = params[0]
            return get_expr(expr_tree, params)
        else:
            params = kwargs
            items = [v for k, v in params.items()]
            return get_expr(expr_tree,*items)
    except Exception as ex:
        print traceback.format_exc()
        raise Exception("Below expression is invalid:\n"
                        "{0}\n"
                        "params {1}\n"
                        "\tdetail:\n\t\t{2}\n{3}".format(expression,params,ex.message,traceback.print_exc(file=sys.stdout)))


