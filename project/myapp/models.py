from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class FH_Location(models.Model):
    case_id = models.IntegerField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location} - {self.case_id}"


class Deceased_Info(models.Model):
    name = models.CharField(max_length=255, null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    date_of_death = models.DateField(null=True)
    male = models.BooleanField(null=True)
    address = models.CharField(max_length=255, null=True)
    ssn = models.CharField(max_length=11, null=True, blank=True)
    nok = models.CharField(max_length=255, null=True)
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_member",null=True)
    case_id= models.ForeignKey(FH_Location, on_delete=models.CASCADE, related_name="case_identification")
    completed = models.BooleanField(null=True, default=False)
    obituary = models.TextField(null=True)

    def __str__(self):
        return f"{self.id}{self.name} - {self.date_of_death}"
    
class Events(models.Model):
    event_deceased_info = models.ForeignKey(Deceased_Info, on_delete=models.CASCADE, related_name="event_deceased_info")
    event_title = models.CharField(max_length=255)
    event_location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    duration = models.FloatField(null=True)
    #add duration/length of time

    
    def __str__(self):
        return f"{self.date} - {self.event_deceased_info} - {self.event_title} - {self.event_location} - {self.duration} - {self.id}"
    
class Finances(models.Model):
    finance_deceased_info = models.ForeignKey(Deceased_Info, on_delete=models.CASCADE, related_name="finance_deceased_info")
    name = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    notes = models.CharField(max_length=255, null=True) 
    quantity = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.category}, {self.price}"

    # remaining balance
    # paid in full
    # remember to migrate
    # Refer to line 28 null = true
