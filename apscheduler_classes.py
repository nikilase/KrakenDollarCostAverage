from dataclasses import field, dataclass
from datetime import datetime
from typing import Any

from apscheduler.schedulers.base import BaseScheduler


@dataclass
class CronSchedule:
    """
    A Dataclass for the Cron Scheduler in APScheduler

    All date and time attributes can be stored in a string with ranges, intervals or just a value.

    For a job being executed every day at 17:00 you can use
            hour="17"
            minute="0"
    If you want to run it every 15 minutes you could use
            minute="0/15"
    If you want to run it every 15 minutes starting at minute 5 (so at minute 5, 20, 35 and 50) you can use
            minute="5/15"
    To run it every 2 hours between 8:00 and 16:00 use
            hour="8-16/2"

    Start and End Dates can be another restriction to only run the jobs after the specified Start Date or until the
    specified End Date. This can be a datetime object or a datetime string e.g. '2024-03-22 14:30:00'

    For more reference see https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html


    Attributes:

    - :class:`str | int` year --> 4-digit year
    - :class:`str | int` month --> month (1-12)
    - :class:`str | int` day --> day of month (1-31)
    - :class:`str | int` week --> ISO week (1-53)
    - :class:`str | int` day of week --> number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    - :class:`str | int` hour --> hour (0-23)
    - :class:`str | int` minute --> minute (0-59)
    - :class:`str | int` second --> second (0-59)
    - :class:`str | datetime` start_date --> earliest possible date/time to trigger on (inclusive)
    - :class:`str | datetime` end_date --> latest possible date/time to trigger on (inclusive)
    """

    schedule_type: str = field(init=False, default="cron")
    year: str | int = None
    month: str | int = None
    day: str | int = None
    week: str | int = None
    day_of_week: str | int = None
    hour: str | int = None
    minute: str | int = None
    second: str | int = None
    start_date: str | datetime = None
    end_date: str | datetime = None


def add_job(
    scheduler: BaseScheduler,
    job: Any,
    job_id: str,
    job_sched: CronSchedule,
):
    scheduler.add_job(
        job,
        id=job_id,
        trigger=job_sched.schedule_type,
        year=job_sched.year,
        month=job_sched.month,
        day=job_sched.day,
        week=job_sched.week,
        day_of_week=job_sched.day_of_week,
        hour=job_sched.hour,
        minute=job_sched.minute,
        second=job_sched.second,
        start_date=job_sched.start_date,
        end_date=job_sched.end_date,
    )
