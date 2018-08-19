x=dict(
    contact=("object",
             False,
             dict(
                 tel="text",
                 fax="text",
                 email="text",
                 address="text"
             )
             ),
    map_location=("object",
                  False,
                  dict(
                      latitude="number",
                      longitude="number"
                  )),
    test=("text", True)
)
def extends_dict(data,*args,**kwargs):
    ret= data.copy()
    x=kwargs
    if type(args) is tuple and args.__len__()>0:
       x =  args[0]
    ret.update(x)
    return ret

class fx(object):
    @property
    def name(self):
        return "XX"
    @name.setter
    def set_name(self,v):
        print v
    @name.getter
    def get_name(self):
        return "CCCCC"


