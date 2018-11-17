"""

"""
class PipelineStage(object):
    def __init__(self):
        self.__stage__={}
    @property
    def stage(self):
        if self.__stage__==None:
            self.__stage__={}
        return self.__stage__
class Project(PipelineStage):
    def __init__(self,*args,**kwargs):
        import pydoc
        super(Project,self).__init__()
        data=kwargs
        if args.__len__()>0:
            for item in args:
                self.__add_item__(item)
    def __add_item__(self,item):
        import pydoc
        if item.__dict__.has_key ("__alias__"):
            self.stage.update ({
                item.__dict__["__alias__"]: pydoc.get_field_expr (item)
            })
        else:
            self.stage.update ({
                pydoc.get_field_expr (item, True): 1
            })
        return self
    def __lshift__(self, other):
        return self.__add_item__(other)
    def append(self,other):
        return self.__add_item__ (other)
class Match(PipelineStage):
    def __init__(self,expr,*args,**kwargs):
        import pydoc
        import expression_parser
        if isinstance(expr,pydoc.Fields):
            self.stage=pydoc.get_field_expr(expr,True)
        elif type(expr) in [str,unicode]:
            self.stage=expression_parser.to_mongobd_match(expr,*args,**kwargs)
class AddFields(Project):
    pass






