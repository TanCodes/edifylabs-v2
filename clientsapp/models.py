"""
>> DB FOR CLIENTS ->
"""

from django.db import models
# Create your models here.


class Course(models.Model):
    title = models.CharField(" 📌 Title ", max_length=100)
    desc = models.CharField(
        "💬 Small Message?", max_length=100, blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


GENDER_client = (
    ('F', 'Female'),
    ('M', 'Male'),
    ('O', 'Others')
)


class Clients(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, null=True, choices=GENDER_client , blank=True)
    company_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=100)
    contact = models.CharField(max_length=13)
    date_of_birth = models.CharField(max_length=100)
    address = models.TextField(max_length=150, null=True)
    coaching_type_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.coaching_type_course})"
    
    class Meta:
        ordering = ('-date_added', )
