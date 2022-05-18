from asyncio import FastChildWatcher
from django.db    import models
from utils.models import TimeStampModel

class Users(TimeStampModel):
    name = models.CharField(max_length=45,unique=True)
    password = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=250, default=False)

    class Meta:
        db_table = "user"