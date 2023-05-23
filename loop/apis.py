from uuid import uuid4
from .classes import ReportStatus
from .models import ReportStat
from .repos import ReportRepo
from .services import ReportService
from .task_executors import ReportExecutor, runInBg
from .utils import DateUtils


class ReportApis:
    @staticmethod
    def get(reportId:str):
        reportStat = ReportRepo.getStat(reportId)
        if reportStat is None:
            return {"ok": False, "msg": "reportId do not exist"}
        
        res = {"ok": True,
                "status": reportStat.status.name, 
                "version": reportStat.version,
                "startedAt": reportStat.runAt, 
                "id": reportStat.id,
                "timeTaken": DateUtils.toIsoFormat(DateUtils.curUtcEpoch() - reportStat.runAt),
                "filename": None
            }
        if reportStat.status == ReportStatus.Complete:
            res |= {
                "timeTaken": DateUtils.toIsoFormat(
                    reportStat.completedAt - reportStat.runAt
                ),
                "filename": f"report-{reportStat.id}-v{reportStat.version}",
            }
        return res
    

    @staticmethod
    def generate():
        reportStat = ReportStat(row={
            ReportStat._Id: str(uuid4()),
            ReportStat._RunAt: DateUtils.curUtcEpoch(),
            ReportStat._Version: 0,
            ReportStat._Status: ReportStatus.Running.value
        })
        print("-------inside first gen function-------")
        ReportRepo.saveStat(reportStat)
        print("------- inside first func after saving report stats-----")
        #runInBg(ReportExecutor, ReportService.generate, reportStat,reportStat.runAt)
        ReportService.generate(reportStat)
        print("-------- done generating report ---------")
        return {"ok": True, "version": reportStat.version,
                "startedAt": reportStat.runAt, "id": reportStat.id,
                "status": reportStat.status.name, "timeTaken": None, "filename": None
            }
