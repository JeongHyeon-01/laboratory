from django.db    import models
from utils.models import TimeStampModel

class Users(TimeStampModel):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=250)

    class Meta:
        db_table = "user"