class MissingFields(Exception):
    def __init__(self,fields,index = None,data = None,parent = None):
        self.parent_field = None
        self.parent_caption = None
        msg = "{0} is require "
        plural_msg = "These {0} are require "
        if index != None:
            if parent != None:
                msg = "{0} is require at "+ parent
            else:
                msg = "{0} is require at row ="+index.__str__()
        if index != None:
            if parent != None:
                plural_msg = "These {0} are require at "+parent
            else:
                plural_msg = "These {0} are require at row ="+index.__str__()

        if list(fields).__len__()==1:
            self.message = msg.format(list(fields)[0])
        else:
            self.message = plural_msg.format(",".join(list(fields)))
        if parent != None:
            self.parent_field = parent
            self.parent_caption = parent+"[" + index.__str__()+"]"
        self.fields = list(fields)
        self.index = index
        self.data = data
        super(MissingFields, self).__init__(self.message)
class InvalidDataFields(Exception):
    def __init__(self,field,receive_data_type,expected_data_type,index = None,data = None,parent = None):
        self.parent_field = None
        self.parent_caption = None
        msg = "{0} is invalid data type. The expected data types is {1}, but receive {2}"
        if parent != None:
            msg = "{0} is invalid data type. The expected data types is {1}, but receive {2} at "+parent
        self.message = msg.format(field,expected_data_type,receive_data_type)
        if isinstance(field,list):
            self.fields = field
        else:
            self.fields = [field]
        self.expected_data_type = expected_data_type
        self.receive_data_type =receive_data_type
        self.index = [index]
        self.data =data
        self.parent_caption = parent
        self.parent_field = parent
        super(InvalidDataFields, self).__init__(self.message)


