"""

"""


class PipelineStage(object):
    def __init__(self):
        self.__stage__ = {}

    @property
    def stage(self):
        if self.__stage__ == None:
            self.__stage__ = {}
        return self.__stage__


class Project(PipelineStage):
    def __parse__(self, data):
        import pydoc
        import expression_parser
        ret = {}
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, pydoc.Fields):
                    ret.update({
                        k: pydoc.get_field_expr(v)
                    })
                elif isinstance(v, dict):
                    ret.update({
                        k: self.__parse__(v)
                    })
                elif isinstance(v, tuple):
                    _v = v[0]
                    _p = [x for x in v if v.index(x) > 0]
                    ret.update({
                        k: expression_parser.to_mongobd()
                    })
                elif isinstance(v, pydoc.Fields):
                    if v.__dict__.has_key("__alias__"):
                        ret.update({
                            v.__dict__["__alias__"]: pydoc.get_field_expr(v)
                        })
                    else:
                        ret.update({
                            pydoc.get_field_expr(v, True): 1
                        })
        return ret

    def __init__(self, *args, **kwargs):

        import pydoc
        import expression_parser
        self.__stage__ = {}
        data = kwargs
        if args.__len__() > 0:
            for item in args:
                if type(item) in [str, unicode]:
                    self.__stage__.update({
                        expression_parser.to_mongobd(item): 1
                    })
                elif isinstance(item, tuple):
                    _v = item[0]
                    _p = tuple([x for x in item if item.index(x) > 0])
                    self.__stage__.update({
                        expression_parser.to_mongobd(_v, *_p): 1
                    })
                elif isinstance(item, dict):
                    self.__stage__.update(self.__parse__(item))
                elif isinstance(item, pydoc.Fields):

                    if item.__dict__.has_key("__alias__"):
                        self.__stage__.update({
                            item.__dict__["__alias__"]: pydoc.get_field_expr(item)
                        })
                    else:
                        right = pydoc.get_field_expr(item, True)
                        if type(right) in [str, unicode]:
                            self.__stage__.update({
                                right: 1
                            })
                        elif isinstance(right, dict):
                            self.__stage__.update(right)

            return

            data = args[0]

        for k, v in data.items():
            if type(v) in [str, unicode]:
                self.__stage__.update({
                    k: expression_parser.to_mongobd(v)
                })
            elif isinstance(v, tuple):
                _v = v[0]
                _p = tuple([x for x in v if v.index(x) > 0])
                self.__stage__.update({
                    k: expression_parser.to_mongobd(_v, *_p)
                })
            elif isinstance(v, pydoc.Fields):
                if v.__dict__.has_key("__alias__"):
                    self.__stage__.update({
                        k: pydoc.get_field_expr(v, True)
                    })
                else:
                    self.__stage__.update({
                        k: pydoc.get_field_expr(v, True)
                    })

    def __add_item__(self, item):
        import pydoc
        if item.__dict__.has_key("__alias__"):
            self.stage.update({
                item.__dict__["__alias__"]: pydoc.get_field_expr(item)
            })
        else:
            self.stage.update({
                pydoc.get_field_expr(item, True): 1
            })
        return self

    def __lshift__(self, other):
        return self.__add_item__(other)

    def append(self, other):
        return self.__add_item__(other)


class Match(PipelineStage):
    def __init__(self, expr, *args, **kwargs):
        import pydoc
        import expression_parser
        if isinstance(expr, pydoc.Fields):
            self.__stage__ = pydoc.get_field_expr(expr, True)
        elif type(expr) in [str, unicode]:
            self.__stage__ = expression_parser.to_mongobd_match(expr, *args, **kwargs)


class AddFields(Project):
    pass


class Lookup(PipelineStage):
    def __init__(self, coll, local_field_or_let, foreign_field_or_pipeline, alias):
        import pydoc
        import expression_parser
        import pyquery
        pipeline = None
        local_field = None
        foreign_field = None
        let = None
        is_use_pipeline = False
        if isinstance(foreign_field_or_pipeline, pyquery.query):
            pipeline = foreign_field_or_pipeline
            let = local_field_or_let
            is_use_pipeline = True
        elif isinstance(foreign_field_or_pipeline, pydoc.Fields):
            foreign_field = pydoc.get_field_expr(foreign_field_or_pipeline, True)
            local_field = local_field_or_let
        elif type(foreign_field_or_pipeline) in [str, unicode]:
            foreign_field = foreign_field_or_pipeline
            local_field = local_field_or_let
        if not is_use_pipeline:
            self.__lookup__(coll, local_field, foreign_field, alias)
        else:
            self.__lookup_with_pipeline(coll, let, pipeline, alias)

    def __lookup__(self, coll, localField, foreignField, alias):
        import pydoc
        import expression_parser
        _CC = coll
        _LF = localField
        _FF = foreignField
        if type(coll) not in [str, unicode]:
            raise Exception("'coll' must be 'str' or 'unicode'")
        if type(alias) not in [str, unicode]:
            raise Exception("'alias' must be 'str' or 'unicode'")
        if isinstance(localField, pydoc.Fields):
            _LF = pydoc.get_field_expr(_LF, True)
        if isinstance(foreignField, pydoc.Fields):
            _FF = pydoc.get_field_expr(_FF, True)
        self.__stage__ = {
            "from": coll,
            "localField": _LF,
            "foreignField": _FF
        }
        return self

    def __lookup_with_pipeline(self, coll, let, pipeline, alias):
        import pyquery
        import pydoc
        import expression_parser
        _l = let
        if type(coll) not in [str, unicode]:
            raise Exception("'coll' must be 'str' or 'unicode'")
        if type(alias) not in [str, unicode]:
            raise Exception("'alias' must be 'str' or 'unicode'")
        if not (pipeline, pyquery.query):
            raise Exception("'pipeline' must be query")
        if isinstance(let, tuple):
            _l = let[0]
            _params = tuple([x for x in let if let.index(x) > 0])
            _l = expression_parser.to_mongobd(_l, *_params)
        elif isinstance(let, pydoc.Fields):
            _l = pydoc.get_field_expr(_l, True)
        elif type(let) in [str, unicode]:
            _l = expression_parser.to_mongobd(_l)
        self.__stage__ = {
            "from": coll,
            "pipeline": pipeline.pipeline,
            "as": alias
        }
        if let != None:
            self.__stage__.update({"let": let})


class Unwind(PipelineStage):
    def __init__(self, expr, includeArrayIndex=None, preserveNullAndEmptyArrays=None):
        import pydoc
        """
        {
          $unwind:
            {
              path: <field path>,
              includeArrayIndex: <string>,
              preserveNullAndEmptyArrays: <boolean>
            }
        }
        :param expr:
        :param args:
        """
        if type(expr) in [str, unicode]:
            self.__stage__ = {
                "path": "$" + expr
            }
        elif isinstance(expr, pydoc.Fields):
            self.__stage__ = {
                "path": pydoc.get_field_expr(expr)
            }
        if includeArrayIndex != None:
            self.__stage__.update({
                "includeArrayIndex": includeArrayIndex
            })
        if preserveNullAndEmptyArrays != None:
            self.__stage__.update({
                "preserveNullAndEmptyArrays": preserveNullAndEmptyArrays
            })


class BucketAuto(PipelineStage):
    def __init__(self, groupBy, buckets, output, granularity=None, *args, **kwargs):
        import pydoc
        import expression_parser
        _groupBy = groupBy
        _buckets = buckets
        _output = output
        _granularity = granularity

        if type(groupBy) in [str, unicode]:
            _groupBy = expression_parser.to_mongobd(groupBy, *args, **kwargs)
        elif isinstance(groupBy, pydoc.Fields):
            _groupBy = pydoc.get_field_expr(groupBy)
        if type(output) in [str, unicode]:
            _output = output
        elif isinstance(output, pydoc.Fields):
            _output = pydoc.get_field_expr(output)
        self.__stage__ = {
            "groupBy": _groupBy,
            "buckets": _buckets,
            "output": _output
        }
        if granularity != None:
            self.__stage__.update({
                "granularity": granularity
            })


class Bukcet(PipelineStage):
    def __init__(self, groupBy, boundaries, default, output, *args, **kwargs):
        import pydoc
        import expression_parser
        _groupBy = groupBy
        _boundaries = boundaries
        _output = output
        _default = default

        if type(groupBy) in [str, unicode]:
            _groupBy = expression_parser.to_mongobd(groupBy, *args, **kwargs)
        elif isinstance(groupBy, pydoc.Fields):
            _groupBy = pydoc.get_field_expr(groupBy)
        if type(output) in [str, unicode]:
            _output = output
        elif isinstance(output, pydoc.Fields):
            _output = pydoc.get_field_expr(output)
        if type(default) in [str, unicode]:
            _default = expression_parser.to_mongobd(default, *args, **kwargs)
        elif isinstance(default, pydoc.Fields):
            _default = pydoc.get_field_expr(default)
        self.__stage__ = {
            "groupBy": _groupBy,
            "boundaries": boundaries,
            "output": _output,
            "default": "default"
        }


class Count(PipelineStage):
    def __init__(self, field=None, *args, **kwargs):
        import pydoc
        import expression_parser
        if field == None:
            field = "ret"
        if isinstance(field, pydoc.Fields):
            self.__stage__ = pydoc.get_field_expr(field, True)
        else:
            self.__stage__ = field


class Facet(PipelineStage):
    def __init__(self, *args, **kwargs):
        import pyquery
        data = kwargs
        self.__stage__ = {}
        if kwargs == {}:
            data = args[0]
        for k, v in data.items():
            if isinstance(v, pyquery.query):
                self.__stage__.update({
                    k, v.pipeline
                })
            else:
                raise Exception("'{0}' must be query")


class Group(PipelineStage):
    def __init__(self, _id, selector, *args, **kwargs):
        import pydoc
        import expression_parser
        __id = _id

        if type(_id) in [str, unicode]:
            __id = expression_parser.to_mongobd(_id, *args, **kwargs)
        elif isinstance(_id, pydoc.Fields):
            __id = pydoc.get_field_expr(_id)
        _selector = {
            "_id": __id
        }
        if not isinstance(selector, dict):
            raise Exception("'selector' must be 'dict'")
        for k, v in selector.items():
            _k = k
            if isinstance(k, pydoc.Fields):
                _k = pydoc.get_field_expr(k, True)
            if type(v) in [str, unicode]:
                _selector.update({
                    _k: expression_parser.to_mongobd(v, *args, **kwargs)
                })
            elif isinstance(v, pydoc.Fields):
                _selector.update({
                    _k: pydoc.get_field_expr(v)
                })
        self.__stage__ = _selector


class ReplaceRoot(PipelineStage):
    def __init__(self, expr, *args, **kwargs):
        import pydoc
        import expression_parser
        if type(expr) in [str, unicode]:
            self.__stage__ = {"newRoot": expression_parser.to_mongobd(expr, *args, **kwargs)}
        elif isinstance(expr, pydoc.Fields):
            self.__stage__ = {"newRoot": pydoc.get_field_expr(expr)}
        elif isinstance(expr, dict):
            data = {}
            for k, v in expr.items():
                _k = k
                if isinstance(k, pydoc.Fields):
                    _k = pydoc.get_field_expr(k, True)
                data.update({
                    _k: pydoc.get_field_expr(v)
                })
            self.__stage__ = {"newRoot": data}


class Sort(PipelineStage):
    def __init__(self, *args, **kwargs):
        import pydoc
        import expression_parser
        data = {}
        if args.__len__() > 0:
            for item in args:
                data.update(item)
        else:
            for k, v in kwargs.items():
                if type(k) in [str, unicode]:
                    data.update({
                        k: v
                    })
                elif isinstance(k, pydoc.Fields):
                    data.update({
                        pydoc.get_field_expr(k, True): v
                    })
        self.__stage__ = data





