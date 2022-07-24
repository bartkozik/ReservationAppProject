from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)



class Room(models.Model):
    name = models.CharField(max_length=225, unique=True)
    capacity = models.IntegerField(default=200)
    screen_avail = models.BooleanField(default=False)


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date')



