from .config_keeper import ConfigKeeper
from .db import get_db
from .models import *
from .utils import WeekDay
import pandas as pd

def inQueryStr(params:list):
    if len(params) == 1:
        return f"= '{params[0]}'"
    joinedParams = ", ".join([f"'{str(param)}'" for param in params])
    return f"IN ( {joinedParams} )"


class StoreRepo:

    @staticmethod


    @staticmethod
    def getSortedPolledStats(storeIds:list[int], fromTimeUtcEpoch:int, toTimeUtcEpoch:int):
        db = get_db()

        # def storeStoredPolledStatus():
        #     df = pd.read_csv('./data/store_status.csv')
        #     df = df[:1000]
        #     for i,row in df.iterrows():
        #         db.execute(f"INSERT INTO {PolledStat.table()} (store_id,timestamp_utc, status) VALUES (%s, %s, %s)",
        #             (row['store_id'],row['timestamp_utc'], row['status']))
        #         print("-------------data stored-------------")


        fromTimeUtc = DateUtils.toDateTimeIsoFormat(fromTimeUtcEpoch)
        toTimeUtc = DateUtils.toDateTimeIsoFormat(toTimeUtcEpoch)

        
        stats:list = []

        batchNo = 0
        batchSize = ConfigKeeper.asInt('POLL_STAT_DBFETCH_BATCH_SIZE')
        while True:
            skip = batchNo * batchSize
            _stats = db.execute(
                " ".join((
                    f"SELECT * FROM poll WHERE storeId {inQueryStr(storeIds)} AND timestampUtc >= '{fromTimeUtc}'",
                    f"AND timestampUtc < '{toTimeUtc}' ORDER BY timestampUtc LIMIT ? OFFSET ?"
                )),
                (batchSize, skip)
            ).fetchall()
            
            batchNo += 1

            if _stats is None:
                _stats = []
            
            if len(_stats) == 0:
                break

            else:
                stats += _stats

        
        print(sortedPolledStats)
        sortedPolledStats:dict[int, list[PolledStat]] = {}
        for row in stats:
            stat = PolledStat(row)
            if stat.storeId not in sortedPolledStats:
                sortedPolledStats[stat.storeId] = [stat]
            else:
                sortedPolledStats[stat.storeId].append(stat)
        
        return sortedPolledStats
        

    @staticmethod
    def getStoreSchedules(storeIds:list[int], weekDay:WeekDay|None):
        db = get_db()

        # def storeStoreSchedules():
        #     df = pd.read_csv('./data/business_hour.csv')
        #     df = df[:1000]
        #     for i,row in df.iterrows():
        #         db.execute(f"INSERT INTO {StoreSchedule.table()} (store_id,dayOfWeek, start_time_local, end_time_local) VALUES (%s, %s, %s, %s)",
        #             (row['store_id'], row['day'], row['start_time_local'], row['end_time_local']))
        #         print("-------------data stored-------------")

        schedules = db.execute(
            " ".join((
                f"SELECT * FROM businessHour WHERE storeId {inQueryStr(storeIds)}",
                "" if weekDay is None else f"AND day_of_Week = {weekDay.value}",
            ))
        ).fetchall()

        if schedules is None:
            schedules = []

        schedulesDict:dict[int, dict[WeekDay, list[StoreSchedule]]] = {}
        for row in schedules:
            schedule = StoreSchedule(row)
            if schedule.storeId not in schedulesDict:
                schedulesDict[schedule.storeId] = {}

            if schedule.dayOfWeek not in schedulesDict[schedule.storeId]:
                schedulesDict[schedule.storeId][schedule.dayOfWeek] = [schedule]
            else:
                schedulesDict[schedule.storeId][schedule.dayOfWeek].append(schedule)

        for storeId in storeIds:
            if storeId not in schedulesDict:
                schedulesDict[storeId] = {}

            if weekDay is None:
                for weekDayItr in WeekDay:
                    if weekDayItr not in schedulesDict[storeId]:
                        schedulesDict[storeId][weekDayItr] = [StoreSchedule.dummyFullDaySchedule(storeId, weekDayItr)]

            elif weekDay not in schedulesDict[storeId]:
                schedulesDict[storeId] = {weekDay: [StoreSchedule.dummyFullDaySchedule(storeId, weekDay)]}
        return schedulesDict
    

    @staticmethod
    def getTzSortedStores(skip, limit):
        db = get_db()
        # def storeTzSortedStoes():
        #     df = pd.read_csv('./data/time_zone.csv')
        #     df = df[:1000]
        #     for i,row in df.iterrows():
        #         db.execute(f"INSERT INTO {StoreSchedule.table()} (store_id,timezone_str) VALUES (%s, %s, %s)",
        #             (row['store_id'], row['timezone_str']))
        #         print("-------------data stored-------------")

        tzs = db.execute(
            "SELECT * FROM TimeZone ORDER BY timezoneStr LIMIT ? OFFSET ?",
            (limit, skip)
        ).fetchall()

        if tzs is None:
            tzs = []

        print("------- inside 3rd func init --------")
        return [StoreInfo(row) for row in tzs]
    


class ReportRepo:
    @staticmethod
    def getStat(reportId:str):
        db = get_db()
        stat = db.execute(
            f"SELECT * from {ReportStat.table()} WHERE {ReportStat._Id} = '{reportId}'",
        ).fetchone()

        return None if stat is None else ReportStat(stat)
    
    @staticmethod
    def saveStat(stat:ReportStat):  # sourcery skip: raise-specific-error
        db = get_db()
        error = True
        try:
            # df = pd.DataFrame(stat.id,stat.status.value,stat.runAt, stat.version)
            # print(stat.id, stat.status.value,stat.runAt,stat.version)
            db.execute(
                f"INSERT INTO report_stat ({ReportStat._Id}, {ReportStat._Status}, {ReportStat._RunAt}, {ReportStat._Version}) VALUES (?, ?, ?, ?)",
                (stat.id, stat.status.value, stat.runAt, stat.version)
            )
            db.commit()
            error = False
        except db.IntegrityError:
            db.execute(
                f"UPDATE report_stat SET {ReportStat._Status} = ?, {ReportStat._CompletedAt} = ? WHERE {ReportStat._Id} = ?",
                (stat.status.value, stat.completedAt, stat.id)
            )
            db.commit()
            error = False

        if error:
            raise Exception("ReportStat:save Error")  