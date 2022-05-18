from django.db import models
from users.models import Users
from utils.models import TimeStampModel

class Questions(TimeStampModel):
    title = models.CharField(max_length=45),
    content = models.TextField()
    user = models.ForeignKey(Users,on_delete=models.CASCADE)

    class Meta:
        db_table = 'question'

class Comments(TimeStampModel):
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.Users',on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'comment'

class Likes(models.Model):
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    user = models.ForeignKey('users.Users',on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        db_table = 'like'

