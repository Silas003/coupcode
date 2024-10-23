from django.db import models
from uuid import uuid4
from accounts.models import CustomUser

class Bet(models.Model):
    class Results(models.TextChoices):
        WON="won"
        LOST="lost"
        NA="na"
    
    class SelectionChoice(models.TextChoices):
        HEAD='HEAD'
        TAIL='TAIL'


    id=models.UUIDField(primary_key=True,default=uuid4)
    date_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name="user_bet")
    stake=models.FloatField()
    stake_return=models.FloatField(null=True,blank=True)
    selection=models.CharField(max_length=10,choices=SelectionChoice.choices)
    pc_selection=models.CharField(max_length=10,choices=SelectionChoice.choices)
    result=models.CharField(choices=Results.choices,default=Results.NA,max_length=30)

    def __str__(self):
        return self.result
    
    class Meta:
        verbose_name = "Bet"


class History(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    previous_bets=models.ManyToManyField(Bet,blank=True)
    user=models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name="user_history")
    last_modified=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "History"