# -*- coding: utf-8 -*-
import datetime
import pymqr
import uuid
@pymqr.documents.EmbededDocument()
class AcadameDetail(object):
    def __init__(self):
        self.RecId = str,None,None,uuid.uuid4
        self.SeniorityFrom = str
        self.SeniorityTo = str
        self.Coefficient = str
        self.Salary =float
        self.CreatedOn = datetime.datetime,None,None,datetime.datetime.now
        self.CreatedBy = str
        self.ModifiedOn = datetime.datetime
        self.ModifiedBy = str
@pymqr.documents.Collection("acadame")
class Acadame(object):
    def __init__(self):
        self.Code = str, True
        self.Name = str
        self.FoName = str
        self.Range = int
        self.Ordinal = int
        self.Note = str
        self.IsFix =int
        self.Coeff = int
        self.AffectedDate = int
        self.Lock = bool
        self.CreatedOn = datetime.datetime
        self.CreatedBy = str
        self.ModifiedOn = datetime.datetime
        self.ModifiedBy = str
        self.details = AcadameDetail
