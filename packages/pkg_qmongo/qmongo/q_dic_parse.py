def parse_to_mongo_dict(value,*params):
    from . import helpers
    if value==1 or value ==0:
        return value
    elif type(value) in [unicode,str]:
        return helpers.expr.get_calc_expr(value, *params)
    elif type(value) is dict:
        ret ={}
        for k,v in value.items():
            ret.update({k:parse_to_mongo_dict(v,*params)})
        return ret
