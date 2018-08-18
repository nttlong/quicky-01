from bson.codec_options import CodecOptions
class __obj_fields__(object):
    pass
class __obj_model__(object):
    def __init__(self,name):
        self.__name__=name
        self.__QR__ = None
        self.fields = __obj_fields__()
        self.__aggregate__=None
    @property
    def query(self,context = None):
        if context == None:
            from . import db_context
            context = db_context.get_db_context()
        if context == None:
            raise (Exception("Please use:\n"
                             "import qmongo\n"
                             "qmongo.set_db_context(host=..,port=..,user=..,password=..,name=..."))
        from . import database

        ret = database.QR()
        ret.db = context.db
        ret._codec_options = CodecOptions()
        return ret.collection(self.__name__)
    @property
    def objects(self,filter = None,*args,**kwargs):
        return self.query.objects(filter,*args,**args)
    def set_session(self,session):
        self.query.set_session(session)
        return self
    @property
    def aggregate(self):
        if self.__aggregate__ == None:
            self.__aggregate__ =self.query.aggregate()
        return self.__aggregate__
    def project(self,*args,**kwargs):
        self.aggregate.project(*args,**kwargs)
        return self
    def lookup(self,source,local_field,foreign_field,alias):
        self.aggregate.lookup(source.__name__,local_field,foreign_field, alias)
        return self
    def join(self,source,local_field,foreign_field, alias):
        self.aggregate.join(source.__name__,local_field,foreign_field, alias)
        return self
    def left_join(self,source,local_field,foreign_field, alias):
        self.aggregate.left_join(source.__name__,local_field,foreign_field, alias)
    def insert(self,*args,**kwargs):
        return self.query.insert(*args,**kwargs)
    def insert_one(self,*args,**kwargs):
        return self.insert_one(*args,**kwargs)
    def update(self,data,*args,**kwargs):
        return self.query.update(data,*args,**kwargs)
    def delete(self,expression,*arg,**kwargs):
        return self.query.delete(expression,*arg,**kwargs)
    def find(self,expression,*args,**kwargs):
        return self.query.find(expression,*args,**kwargs)
    @property
    def object(self):
        return self.aggregate.get_object()
    def sort(self, *args, **kwargs):
        self.aggregate.sort(*args, **kwargs)
        return self
    def check_field(self,field):
        self.aggregate.check_fields(field)
        return self
    def count(self,alais = None):
        if alais == None:
            alais = self.__name__+"_____count"
        return self.aggregate.count(alais)
    def skip(self,len):
        self.aggregate.skip(len)
        return self
    @property
    def cursors(self):
        return self.aggregate.cursor_list()
    @property
    def item(self, *args, **kwargs):
        return self.aggregate.get_item()
    @property
    def documents(self):
        return  self.aggregate.get_all_documents()
    @property
    def items(self):
        return self.aggregate.get_list()



















