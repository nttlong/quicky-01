def parse_to_mongo_dict(value,*params):
    from . import helpers
    if value==1 or value ==0:
        return value
    elif type(value) in [unicode,str]:
        return helpers.expr.get_calc_expr(value, *params)
    elif type(value) is dict:
        ret ={}
        for k,v in value.items():
            x = parse_to_mongo_dict(v,*params)
            if type(x) is dict:
                for k1,v1 in x.items():
                    ret.update({k+"."+k1:v1})
            else:
                ret.update({k: x})
        return ret
