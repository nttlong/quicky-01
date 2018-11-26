VERSION = [1, 0, 0, "beta", 2]


def get_version():
    return VERSION[0].__str__ () + \
           "." + VERSION[1].__str__ () + \
           "." + VERSION[2].__str__ () + \
           "." + VERSION[3].__str__ () + \
           "." + VERSION[4].__str__ ()


from . import exceptions
from . import dmobj


class __GOBBLE__ ():
    @staticmethod
    def consume_data(data, parent):
        fields = []
        if isinstance (data, dict):
            ret = {}
            for k, v in data.items ():
                field_info = __field_info__ (v)
                ret.update ({
                    k: field_info
                })
                if isinstance (field_info.detail, dict):
                    for x, y in field_info.detail.items ():
                        y.parent_field_name = k
                        y.parent = field_info
                    fields.extend ([{k + "." + x: y} for x, y in field_info.detail.items ()])
                    fields.append ({k: field_info})
                else:

                    fields.append ({k: field_info})

            return dict (
                data=ret,
                fields=fields
            )
        else:
            return data

    @staticmethod
    def clone_data(data):
        ret = {}
        if isinstance (data, dict):
            for k, v in data.items ():
                if isinstance (v, dict):
                    ret.update ({
                        k: __GOBBLE__.clone_data (v)
                    })
                else:
                    ret.update ({
                        k: v
                    })
        return ret


class __field_info__ ():
    def __init__(self, params):
        self.is_require = False
        self.data_type = None
        self.detail = None
        self.parent_field_name = None
        self.parent = None
        if isinstance (params, tuple):
            self.data_type = params[0]
            if params.__len__ () > 1:
                self.is_require = params[1]
            if params.__len__ () > 2:
                detail_info = __GOBBLE__.consume_data (params[2], None)
                self.detail = detail_info["data"]
                self.fields = detail_info["fields"]
        else:
            self.data_type = params

    def validate(self, data, parent_name):
        require_fields = set ([x for x, y in self.detail.items () if y.is_require == True])
        # chk_data = __GOBBLE__.clone_data(self.detail)
        # chk_data.update(data)
        # if chk_data == data:
        #     return
        index = 0
        if isinstance (data, list):
            for data_item in data:
                try:
                    self.validate (data_item, parent_name)
                    index += 1
                except exceptions.MissingFields as ex:
                    if ex.parent_caption != None:
                        endfix = ex.parent_caption[parent_name.__len__ () + 1:ex.parent_caption.__len__ ()]
                        raise exceptions.MissingFields (ex.fields, [index, ex.index], data_item,
                                                        parent_name + "[" + index.__str__ () + "]." + endfix)
                    else:

                        raise exceptions.MissingFields (ex.fields, index, data_item, parent_name)

            return

        missing_fields = require_fields.difference (set (data))
        if missing_fields != set ([]):
            if parent_name == None:
                raise exceptions.MissingFields (missing_fields)
            else:
                raise exceptions.MissingFields ([parent_name + "." + x for x in list (missing_fields)])
        object_fields = set ([x for x, y in self.detail.items () if y.detail != None])
        input_object_fields = set (data).intersection (object_fields)
        for item in list (input_object_fields):
            if parent_name != None:
                self.detail[item].validate (data[item], parent_name + "." + item)
            else:
                self.detail[item].validate (data[item], item)

    def validate_data_type(self, data, parent_name):
        check_fields = set (self.detail).intersection (set (data))
        for item in list (check_fields):
            if data[item] != None:
                if self.detail[item].data_type != type (data[item]):
                    if parent_name != None:
                        raise exceptions.InvalidDataFields (parent_name + "." + item, type (data[item]),
                                                            self.detail[item].data_type)
                if isinstance (data[item], dict):
                    if parent_name != None:
                        self.detail[item].validate_data_type (data[item], parent_name + "." + item)
                    else:
                        self.detail[item].validate_data_type (data[item], item)
                elif isinstance (data[item], list):
                    index = 0
                    for data_item in data[item]:
                        try:
                            self.detail[item].validate_data_type (data_item, parent_name + "." + item)
                        except exceptions.InvalidDataFields as ex:
                            if ex.parent_caption == None:
                                raise exceptions.InvalidDataFields (ex.fields, ex.receive_data_type,
                                                                    ex.expected_data_type, index, data_item,
                                                                    parent_name + "." + item + "[" + index.__str__ () + "]")
                            else:
                                ex.index.insert (0, index)
                                raise exceptions.InvalidDataFields (ex.fields, ex.receive_data_type,
                                                                    ex.expected_data_type, ex.index, data_item,
                                                                    ex.parent_caption.replace ("." + item + ".",
                                                                                               "." + item + "[" + index.__str__ () + "]."))
                        index += 1


class __types_wrapper__ (object):
    def __init__(self, *args, **kwargs):
        self.param_by_index = False
        _data_ = None
        if args.__len__ () == 1 and isinstance (args[0], dict):
            _data_ = __GOBBLE__.consume_data (args[0], None)
        elif args.__len__ () > 0:
            _data_ = {}
            index = 0
            for item in args:
                _data_.update ({
                    "params_" + index.__str__ (): item
                })
                index += 1
            _data_ = __GOBBLE__.consume_data (_data_, None)
            self.param_by_index = True
        else:
            _data_ = __GOBBLE__.consume_data (kwargs, None)
        self.fields = _data_["fields"]
        self.data = _data_["data"]
        self.input_params = None

    def validate(self, *args, **kwargs):
        data = kwargs
        if args.__len__ () > 0:
            data = args[0]
        compare_data = __GOBBLE__.clone_data (self.data)
        cmp_inter_data = __GOBBLE__.clone_data (self.data)
        require_fields = require_fields = set ([x for x, y in self.data.items () if y.is_require == True])
        object_fields = set ([x for x, y in self.data.items () if y.detail != None])
        missing_fields = require_fields.difference (set (data))
        if missing_fields != set ([]):
            raise exceptions.MissingFields (missing_fields)
        input_object_fields = set (data).difference (require_fields).intersection (object_fields)
        for item in list (input_object_fields):
            self.data[item].validate (data[item], item)
        compare_data.update (data)
        differ_data = set (compare_data).difference (set (data))
        input_fields = set ([x for x in list (set (data).intersection (set (self.data))) if data[x] != None])
        for item in list (input_fields):
            if type (data[item]) != self.data[item].data_type:
                raise exceptions.InvalidDataFields (item, type (data[item]), self.data[item].data_type)
            if self.data[item].data_type == dict:
                self.data[item].validate_data_type (data[item], item)
        if args.__len__ () > 0:
            data = args[0]

    def build_input_params_and_run(self, *args, **kwargs):
        if self.input_params.__len__ () == 1:
            data = kwargs
            if args.__len__ () > 0:
                data = args[0]

            _data_ = dmobj.pobject(data)
            return self.__caller__ (_data_)
        return self.__caller__ (*args, **kwargs)

    def execute(self, *args, **kwargs):
        if self.param_by_index:
            data_params = {}
            index = 0
            for item in args:
                data_params.update ({
                    "params_" + index.__str__ (): item
                })
                index += 1
            self.validate (data_params)
            return self.build_input_params_and_run (*args, **kwargs)
        else:
            self.validate (*args, **kwargs)

            return self.build_input_params_and_run (*args, **kwargs)

    def wrapper(self, *args, **kwargs):
        import inspect
        self.__caller__ = args[0]
        self.input_params = inspect.getargspec (self.__caller__).args

        return self.execute


def types(*args, **kwargs):
    ret = __types_wrapper__ (*args, **kwargs)
    return ret.wrapper
