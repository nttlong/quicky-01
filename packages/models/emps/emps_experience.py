import pymqr
import datetime
@pymqr.documents.EmbededDocument()
class EmpExperience(object):
    """

    """
    def __init__(self):
        """

        """
        self.BeginDate = (datetime.datetime, True)
        self.EndDate = datetime.datetime
        self.Salary = int
        self.Currency_code =str
        self.EmpTypeCode = str
        self.JobPosCode = str
        self.JobWCode = str
        self.WorkingOn = str
        self.WorkingLocation = str
        self.Address =str
        self.ProfessionCode =str
        self.QuitJobCode = str
        self.Reason = str
        self.RefInfo = str
        self.Note = str
        self.IsNaCompany = str
        self.IsInSection = str