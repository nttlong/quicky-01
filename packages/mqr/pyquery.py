import expression_parser
import mobject
import pycollection
class query():
    def __init__(self,*args,**kwargs):
        if kwargs=={}:
            if args.__len__()==2 and\
                hasattr(args[0],"get_collection") and\
                type(args[1]) in [str,unicode]:
                self.coll=args[0].get_collection(args[1])
            elif args.__len__()==1 and\
                hasattr(args[0],"aggregate") and\
                hasattr(args[0],"database"):
                self.coll=args[0]
        self.pipeline=[]
    def where(self,expr,*args,**kwargs):
        #type:()->pycollection.entity
        return pycollection.entity(self,expression_parser.to_mongobd_match(expr,*args,**kwargs))
    def insert(self,*args,**kwargs):
        # type:()->pycollection.entity
        ret=pycollection.entity(self)
        ret.insert(*args,**kwargs)
        return ret
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
    def find(self):
        return self.coll.find()
    def find_one(self):
        return self.coll.find_one()
    def find_to_object(self):
        ret= self.find_one()
        return mobject.dynamic_object(ret)
    def find_to_objects(self):
        ret= self.find()
        for item in ret:
            yield mobject.dynamic_object(item)
    def set(self,*args,**kwargs):
        ret= pycollection.entity(self)
        ret.set(*args,**kwargs)
        return ret
    def inc(self,*args,**kwargs):
        ret= pycollection.entity()
        ret.inc(*args,**kwargs)
        return ret
    def mul(self,*args,**kwargs):
        ret= pycollection.entity()
        ret.inc(*args,**kwargs)
        return ret
    def push(self,*args,**kwargs):
        ret= pycollection.entity()
        ret.push(*args,**kwargs)
        return ret
    def pull(self,expr,*args,**kwargs):
        ret= pycollection.entity()
        ret.pull(expr,*args,**kwargs)
        return ret
    def addToSet(self,*args,**kwargs):
        ret= pycollection.entity()
        ret.addToSet(*args,**kwargs)
        return ret
    def add_to_set(self,*args,**kwargs):
        return self.addToSet(*args,**kwargs)





