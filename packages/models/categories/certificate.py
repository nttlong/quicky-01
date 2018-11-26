import pymqr
import datetime
@pymqr.documents.Collection("certificate")
class Certificate(object):
    def __init__(self):
        self.Code = str,True
        self.Name = str,True
        self.FName = str
        self.ExpiredTime = int
        self.group_cer_code = str
        self.CersTimeLimit = int
        self.scer_code =str
        self.cers_replace_code =str
        self.Ordinal = int
        self.Note = str
        self.Lock = bool
        self.CreatedOn =datetime,True,datetime.datetime.now
        self.CreatedBy = str, True
        self.ModifiedOn = str
        self.ModifiedBy = datetime.datetime