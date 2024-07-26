from typing import Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler


class Scheduler:
    def __init__(self, scheduler: BackgroundScheduler) -> None:
        self._scheduler: BackgroundScheduler = scheduler()

    def add_job(self, func: Callable, minutes: int, interval='interval'):
        return self._scheduler.add_job(func, interval, minutes=minutes)

    def get_jobs(self):
        return self._scheduler.get_jobs()

    def start_job(self):
        self._scheduler.start()


scheduler = Scheduler(BackgroundScheduler)
