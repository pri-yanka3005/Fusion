from django.db import models
from django.db import models
from applications.globals.models import *
from django.contrib.auth.models import User
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Constants:
    RESPONSE_TYPE = (
        ('Approved', 'Approved'),
        ('Disapproved', 'Disapproved'),
        ('Pending' , 'Pending')
    )



class projects(models.Model): 
    PROJECT_TYPES = (
        ('Research', 'Research'),
        ('Product', 'Product'),
        ('Consultancy', 'Consultancy'),
    )   

    CATEGORY_CHOICES = (
        ('Government', 'Governement'),
        ('Private', 'Private Entity'),
        ('IIITDMJ', 'Institute'),
        ('Other', 'Other'),
    )

    STATUS_CHOICES = (
        ('OnGoing', 'OnGoing'),
        ('Terminated', 'Terminated'),
        ('Completed', 'Completed'),
    )      

    DEPT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('SM', 'School of Management'),
        ('Des', 'Design'),
        ('NS', 'Natural Sciences'),
        ('LA', 'Liberal Arts'),
        ('none', 'None Of The Above'),
    ]

    pid = models.AutoField(primary_key=True)
    name= models.CharField(max_length=600)
    type= models.CharField(max_length=50, choices=PROJECT_TYPES)
    pi_name=models.CharField(max_length=150)
    pi_id=models.CharField(max_length=150)
    sponsored_agency= models.CharField(max_length=500)
    dept=models.CharField(max_length=50, choices=DEPT_CHOICES)
    start_date=models.DateField()
    deadline=models.DateField()
    finish_date=models.DateField(null=True, blank=True)
    status= models.CharField(max_length=50, choices=STATUS_CHOICES)
    file=models.FileField( null=True, blank=True)
    end_report=models.FileField( null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    total_budget=models.IntegerField(default=0)
    rem_budget=models.IntegerField(default=0)
    category=models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    

    def __str__(self):
        return str(self.pid)

    class Meta:
        ordering = ['-pid']


class expenditure(models.Model):
    EXPENDITURE_TYPES = (
        ('Tangible', 'Physical Item'),
        ('Non-tangible', 'Non-tangible Resource'),
    )
    APPROVAL_CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending' , 'Pending')
    )
    id = models.AutoField(primary_key=True)
    file_id=models.IntegerField()
    pid=models.ForeignKey(projects, on_delete=models.CASCADE)
    exptype = models.CharField(max_length=50, choices=EXPENDITURE_TYPES)
    item = models.CharField(max_length=300)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    lastdate = models.DateField(null=True, blank=True)
    mode = models.CharField(max_length=50)
    inventory = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    approval= models.CharField(max_length=50, choices=APPROVAL_CHOICES)

    def clean(self):
        if self.cost <= 0:
            raise ValidationError('Estimated cost must be greater than zero')

        if self.lastdate != '' and self.lastdate < datetime.datetime.now().date():
            raise ValidationError('Last date must not be a past date')
        
    def __str__(self):
        return f"{self.item} ({self.exptype})"

class staff(models.Model):
    DESIGNATION_CHOICES = [
        ('Co-Project Investigator', 'Co-Project Investigator'),
        ('Research Scholar', 'Research Scholar'),
        ('Research Assistant', 'Research Assistant'),
        ('Supporting Staff', 'Supporting Staff'),
        ('Student Intern', 'Student Intern'),
    ]

    QUALIFICATION_CHOICES = [
        ('MTech', 'MTech Student'),
        ('PhD', 'PhD Student'),
        ('Professor', 'Teaching Faculty'),
        ('Other', 'Other Supporting Staff'),
    ]

    DEPT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('SM', 'School of Management'),
        ('Des', 'Design'),
        ('NS', 'Natural Sciences'),
        ('LA', 'Liberal Arts'),
        ('none', 'None Of The Above'),
    ]

    APPROVAL_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending' , 'Pending')
    ]

    id = models.AutoField(primary_key=True)
    file_id=models.IntegerField()
    pid=models.ForeignKey(projects, on_delete=models.CASCADE)
    person = models.CharField(max_length=300)
    uname = models.CharField(max_length=150)
    dept = models.CharField(max_length=50, choices=DEPT_CHOICES)
    qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    stipend = models.DecimalField(max_digits=10, decimal_places=2)
    startdate = models.DateField(null=True, blank=True)
    lastdate = models.DateField(null=True, blank=True)
    desc = models.TextField(blank=True,  null=True)
    file = models.FileField(upload_to='staff_profiles/', blank=True, null=True)
    approval= models.CharField(max_length=50, choices=APPROVAL_CHOICES) 

    def clean(self):
        if self.deadline <= self.startdate:
            raise ValidationError('End date must be after the start date.')
        if self.stipend < 0:
            raise ValidationError('Stipend must be atleast zero')

    def __str__(self):
        return f"{self.person} ({self.uname}) - {self.designation}"

    

# class requests(models.Model):
#     APPROVAL_CHOICES = [
#     ('Approved', 'Approved'),
#     ('Rejected', 'Rejected'),
#     ('Pending' , 'Pending')
#     ]
#     REQUEST_TYPES = [
#     ('Expenditure', 'Expenditure'),
#     ('Staff', 'Staff'),
#     ]
#     id=models.AutoField(primary_key=True)
#     pid= models.ForeignKey(projects, on_delete=models.CASCADE)
#     file_id=models.IntegerField()  
#     request_type=models.CharField(max_length=50, choices=REQUEST_TYPES)
#     rid=models.IntegerField()
#     subject=models.CharField(max_length=300)
#     requestor=models.CharField(max_length=150)
#     holder=models.CharField(max_length=150)
#     approval= models.CharField(max_length=50, choices=APPROVAL_CHOICES) 

#     def __str__(self):
#         return f"{self.pid} ({self.request_type}) - {self.rid}"

#     class Meta:
        ordering = ['-id']


    
class project_access(models.Model):
    id=models.AutoField(primary_key=True)
    lead_id= models.CharField(max_length=150)
    pid= models.ForeignKey(projects, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.lead_id)
    
    class Meta:
        ordering = ['-lead_id']
    
    
    
    

    
