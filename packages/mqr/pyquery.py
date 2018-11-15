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
    def addFields(self,fields,*args,**kwargs):
        """
        :param selectors:
        :param args:
        :param kwargs:
        :return:
        """
        _project={}
        if(isinstance(fields,dict)):
            for k,v in fields.items():
                _project.update({
                    k:expression_parser.to_mongobd(v,*args,**kwargs)
                })
            self.pipeline.append({
                "$addFields":_project
            })
            return self
        else:
            raise Exception("selector must be dict")
    def add_fields(self,fields,*args,**kwargs):
        return self.addFields(fields,*args,**kwargs)
    def match(self,expr,*args,**kwargs):
        self.pipeline.append({
            "$match":expression_parser.to_mongobd_match(expr,*args,**kwargs)
        })
        return self
    def lookup(self,*args,**kwargs):
        return self
    def bucketAuto(self,groupBy,buckets,output,granularity,*args,**kwargs):
        return self
    def bucket_auto(self,groupBy,buckets,output,granularity,*args,**kwargs):
        return self.bucketAuto(groupBy,buckets,output,granularity,*args,**kwargs)
    def bucket(self,groupBy,boundaries,default,output,*args,**kwargs):
        return self
    def count(self,field=None):
        if field==None:
            field="ret"
        self.pipeline.append({
            "$count":field
        })
        return self
    def facet(self,*args,**kwargs):
        return self
    def group(self,selectors, _id=None,*args,**kwargs):
        return self
    def replaceRoot(self):
        return self

