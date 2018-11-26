import pymqr
import datetime

@pymqr.documents.EmbededDocument()
class AwardPlace(object):
    def __init__(self):
        self.Code = str, True
        self.Name = str, True
        self.FoName = str
        self.ordinal = int
        self.note = str
        self.lock = bool
@pymqr.documents.EmbededDocument()
class AwardLevel(object):
    def __init__(self):
        self.Code = str, True
        self.Name = str, True
        self.FoName = str
        self.Ordinal = int
        self.Note = str
        self.Lock = bool
        self.MaxTimesPerYear = str
        self.CreatedOn = datetime.datetime,True,None,datetime.datetime.now
        self.CreatedBy = str,True
        self.ModifiedOn = datetime.datetime
        self.ModifiedBy = str

@pymqr.documents.Collection("award")
class Award(object):
    """
    List of award
    """
    def __init__(self):
        self.Code = str, True
        self.Name = str, True
        self.Name2 = str
        self.Ordinal = int
        self.Note = str
        self.Lock = bool
        self.Level= AwardLevel()
        self.Place = AwardPlace()
        self.award_type = int
        self.IsTeam = bool
        self.CreatedOn = datetime.datetime,True,None,datetime.datetime.now
        self.CreatedBy = str,True
        self.ModifiedOn = datetime.datetime
        self.ModifiedBy = str
