from django.db import models

from clientsapp.models import Course
# Create your models here.


class ScheduleClients(models.Model):
    first_name_S = models.CharField(max_length=100)
    last_name_S = models.CharField(max_length=100)
    coaching_type_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review_call = models.BooleanField(default=False)
    sessions = models.CharField(max_length=100)
    my_time_field = models.TimeField()
    client_count = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.first_name_S} {self.last_name_S} ({self.coaching_type_course})"
    
    
