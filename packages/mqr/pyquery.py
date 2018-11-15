import expression_parser
class query():
    def __init__(self):
        self.pipeline=[]
    def project(self,selectors,*args,**kwargs):
        """
        :param selectors:
        :param args:
        :param kwargs:
        :return:
        """
        _project={}
        if(isinstance(selectors,dict)):
            for k,v in selectors.items():
                _project.update({
                    k:expression_parser.to_mongobd(v,*args,**kwargs)
                })
            self.pipeline.append({
                "$project":_project
            })
            return self
        else:
            raise Exception("selector must be dict")
    def match(self,expr,*args,**kwargs):
        self.pipeline.append({
            "$match":expression_parser.to_mongobd_match(expr,*args,**kwargs)
        })
        return self
