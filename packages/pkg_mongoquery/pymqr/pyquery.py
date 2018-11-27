import expression_parser
import mobject
import pycollection
import pydocs
import pyfuncs


class PageDataItems (object):
    def __init__(self):
        self.page_size = 0
        self.page_index = 0
        self.total_items = 0
        self.total_pages = 0

        self.items = []


class query ():
    def __init__(self, *args, **kwargs):
        import documents
        if kwargs == {}:
            if args.__len__ () == 2:
                if hasattr (args[0], "get_collection"):
                    if type (args[1]) in [str, unicode]:
                        self.coll = args[0].get_collection (args[1])
                    if issubclass (type (args[1]), documents.BaseDocuments):
                        self.coll = args[0].get_collection (args[1].get_collection_name ())
            elif args.__len__ () == 1 and \
                    hasattr (args[0], "aggregate") and \
                    hasattr (args[0], "database"):
                self.coll = args[0]
        self.pipeline = []

    def stages(self, *args, **kwargs):
        import pyaggregatebuilders
        for item in args:
            if isinstance (item, dict):
                self.pipeline.append (item)
            elif isinstance (item, pyaggregatebuilders.Match):
                self.pipeline.append ({
                    "$match": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Project):
                self.pipeline.append ({
                    "$project": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.AddFields):
                self.pipeline.append ({
                    "$addFields": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Lookup):
                self.pipeline.append ({
                    "$lookup": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Unwind):
                self.pipeline.append ({
                    "$unwind": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.BucketAuto):
                self.pipeline.append ({
                    "$bucketAuto": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Bukcet):
                self.pipeline.append ({
                    "$bucket": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Count):
                self.pipeline.append ({
                    "$count": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Facet):
                self.pipeline.append ({
                    "$facet": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Group):
                self.pipeline.append ({
                    "$group": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.ReplaceRoot):
                self.pipeline.append ({
                    "$replaceRoot": item.stage
                })
            elif isinstance (item, pyaggregatebuilders.Sort):
                self.pipeline.append ({
                    "$sort": item.stage
                })

        return self

    def where(self, expr, *args, **kwargs):
        # type:()->pycollection.entity
        if type (expr) is [str, unicode]:
            return pycollection.entity (self, expression_parser.to_mongobd_match (expr, *args, **kwargs))
        elif isinstance (expr, pydocs.Fields):
            return pycollection.entity (self, pydocs.get_field_expr (expr))
        else:
            raise Exception("invalid data type {0}".format(type(expr)))

    def insert(self, *args, **kwargs):
        # type:()->pycollection.entity
        ret = pycollection.entity (self)
        ret.insert (*args, **kwargs)
        return ret

    def project(self, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Project (*args, **kwargs))
        return self

    def addFields(self, fields, *args, **kwargs):
        """
        :param selectors:
        :param args:
        :param kwargs:
        :return:
        """
        _project = {}
        if (isinstance (fields, dict)):
            for k, v in fields.items ():
                _project.update ({
                    k: expression_parser.to_mongobd (v, *args, **kwargs)
                })
            self.pipeline.append ({
                "$addFields": _project
            })
            return self
        else:
            raise Exception ("selector must be dict")

    def add_fields(self, fields, *args, **kwargs):
        return self.addFields (fields, *args, **kwargs)

    def match(self, expr, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (
            pyaggregatebuilders.Match (expr, *args, **kwargs)
        )
        return self

    def sort(self, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (
            pyaggregatebuilders.Sort (*args, **kwargs)
        )
        return self

    def limit(self, num):
        self.stages ({
            "$limit": num
        })
        return self

    def skip(self, num):
        self.stages ({
            "$skip": num
        })
        return self

    def lookup(self, coll, local_field_or_let, foreign_field_or_pipeline, alias):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Lookup (
            coll,
            local_field_or_let,
            foreign_field_or_pipeline,
            alias))
        return self

    def bucketAuto(self, groupBy, buckets, output, granularity=None, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.BucketAuto (
            groupBy,
            buckets,
            output,
            granularity,
            *args,
            **kwargs
        ))
        return self

    def bucket_auto(self, groupBy, buckets, output, granularity=None, *args, **kwargs):
        return self.bucketAuto (groupBy, buckets, output, granularity, *args, **kwargs)

    def bucket(self, groupBy, boundaries, default, output, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Bukcet (
            groupBy,
            boundaries,
            default,
            output,
            *args,
            **kwargs
        ))
        return self
        return self

    def count(self, field=None, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Count (
            field,
            *args,
            **kwargs
        ))
        return self

    def facet(self, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Facet (
            *args, **kwargs
        ))
        return self

    def group(self, _id=None, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.Group (
            _id,
            *args,
            **kwargs
        ))
        return self

    def replaceRoot(self, expr, *args, **kwargs):
        import pyaggregatebuilders
        self.stages (pyaggregatebuilders.ReplaceRoot (
            expr,
            *args,
            **kwargs
        ))
        return self

    def __iter__(self):
        return list (self.items)

    def __rshift__(self, other):
        other = list (self.objects)

    def reset(self):
        self.pipeline = []
        return self

    def find(self):
        return self.coll.find ()

    def find_one(self):
        return self.coll.find_one ()

    def find_to_object(self):
        ret = self.find_one ()
        return mobject.dynamic_object (ret)

    def find_to_objects(self):
        ret = self.find ()
        for item in ret:
            yield mobject.dynamic_object (item)

    def set(self, *args, **kwargs):
        ret = pycollection.entity (self)
        ret.set (*args, **kwargs)
        return ret

    def inc(self, *args, **kwargs):
        ret = pycollection.entity ()
        ret.inc (*args, **kwargs)
        return ret

    def mul(self, *args, **kwargs):
        ret = pycollection.entity ()
        ret.inc (*args, **kwargs)
        return ret

    def push(self, *args, **kwargs):
        ret = pycollection.entity (self)
        ret.push (*args, **kwargs)
        return ret

    def pull(self, expr, *args, **kwargs):
        ret = pycollection.entity (self)
        ret.pull (expr, *args, **kwargs)
        return ret

    def addToSet(self, *args, **kwargs):
        ret = pycollection.entity ()
        ret.addToSet (*args, **kwargs)
        return ret

    def add_to_set(self, *args, **kwargs):
        return self.addToSet (*args, **kwargs)

    @property
    def items(self):
        return self.coll.aggregate (self.pipeline)

    @property
    def objects(self):
        for item in self.items:
            yield mobject.dynamic_object(item)

    @property
    def object(self):
        ret= list(self.items)
        if ret.__len__()>0:
            return mobject.dynamic_object(ret[0])
        else:
            return mobject.dynamic_object({})

    def get_page(self, page_size, page_index):
        _pipeline = [x for x in self.pipeline]
        _pipeline.append ({
            "$count": "ret"
        })
        ret_counts = list (self.coll.aggregate (_pipeline))
        ret = PageDataItems ()
        if ret_counts.__len__ () == 0:
            return ret
        else:
            ret.total_items = ret_counts[0]["ret"]
            ret.page_size = page_size
            ret.page_index = page_index
            ret.total_pages = ret.total_pages / ret.page_size
            if ret.total_pages % ret.page_size > 0:
                ret.total_pages += 1
            self.pipeline.append ({
                "$skip": ret.page_size * (ret.page_index)
            })
            self.pipeline.append ({
                "$limit": ret.page_size
            })
            ret.items = list (self.coll.aggregate (self.pipeline))
            return ret

    def get_page_of_object(self, page_size, page_index):
        import mobject
        ret = self.get_page (page_size, page_index)
        ret.items = [mobject.dynamic_object (x) for x in ret.items]
        return ret
