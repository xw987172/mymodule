# coding: utf8
from datetime import datetime
from datetime import timedelta

class dateutilsclass():

    @staticmethod
    def getDay(n):
        return datetime.now() - timedelta(days=n)