from django.db import models

DEPARTMENT =(
    ('1','CSE'),
    ('2','ECE'),
    ('3','EEE'),
    ('4','MECH'),
    ('5','CIVIL')
)

BLOOD_GROUP = (
    ('1','B+ve'),
    ('2','B-ve'),
    ('3','A+ve'),
    ('4','A-ve'),
    ('5','O+ve'),
    ('6','O-ve'),
    ('7','AB+ve'),
    ('8','AB-ve')
)

EVENTCON_TYPE = (
    ('1','Faculty Development Program'),
    ('2','Department Association Activites'),
    ('3','Value Added Courses Conducted'),
    ('4','Guest Lecture Conducted'),
    ('5','Workshop Conducted')
)

EVENTAT_TYPE = (
    ('1','International Conference'),
    ('2','PSG CARE Program'),
    ('3','Workshop'),
    ('4','Online Course')
)

class File(models.Model):
    my_file = models.FileField(upload_to='')
    file_name = models.CharField(max_length=1000)

class Awards(models.Model):
    facultyname = models.CharField(max_length=100)
    facultyid = models.CharField(max_length=100)
    dateawarded = models.DateField(max_length=8,default=None,null=True)
    awardname = models.CharField(max_length=100)
    awarddescription = models.TextField(max_length=500,null=True)
    department = models.CharField(choices= DEPARTMENT,max_length=100)
    awardedby = models.CharField(max_length=100,null=True)

class Personal(models.Model):
    facultyname = models.CharField(max_length=100)
    facultyid = models.CharField(max_length=100)
    annaid = models.CharField(max_length=100)
    aicteid = models.CharField(max_length=100)
    emailid = models.EmailField(max_length=100,null=True)
    mobileno = models.CharField(max_length=15,null=True)
    dob = models.DateField(max_length=8,default=None,null=True)
    address = models.TextField(max_length=500,null=True)
    bgroup = models.CharField(choices=BLOOD_GROUP,max_length=6,null=True)
    department = models.CharField(choices= DEPARTMENT,max_length=100,null=True)
    ugabout = models.TextField(max_length=500,null=True)
    ugyear = models.CharField(max_length=4,null=True)
    pgabout = models.TextField(max_length=500,null=True)
    pgyear = models.CharField(max_length=4,null=True)
    phdabout = models.TextField(max_length=500,null=True)
    phdyear = models.CharField(max_length=4,null=True)
    ac_name = models.CharField(max_length=100,null=True)
    ac_from = models.DateField(max_length=8,default=None,null=True)
    ac_to = models.DateField(max_length=8,default=None,null=True)
    in_name = models.CharField(max_length=100,null=True)
    in_from = models.DateField(max_length=8,default=None,null=True)
    in_to = models.DateField(max_length=8,default=None,null=True)
    re_name = models.CharField(max_length=100,null=True)
    re_from = models.DateField(max_length=8,default=None,null=True)
    re_to = models.DateField(max_length=8,default=None,null=True)
    aoi = models.TextField(max_length=500,null=True)

class Evcon(models.Model):
    facultyid = models.CharField(max_length=100)
    eventtitle = models.CharField(max_length=100)
    eventtype = models.CharField(choices=EVENTCON_TYPE,max_length=100)
    rpname = models.CharField(max_length=100,null=True)
    rpdesig = models.CharField(max_length=100,null=True)
    rpcompany = models.CharField(max_length=100,null=True)
    rpphone = models.CharField(max_length=15,null=True)
    rpmail = models.EmailField(max_length=100,null=True)
    organizer = models.CharField(max_length=100,null=True)
    date = models.DateField(max_length=8,default=None,null=True)
    nofac = models.CharField(max_length=6,null=True)
    nostud =  models.CharField(max_length=6,null=True)
    dept =  models.CharField(choices=DEPARTMENT,max_length=100)
    eventdesc = models.TextField(max_length=500,null=True)

class Eveat(models.Model):
    facultyid = models.CharField(max_length=100)
    facultyname = models.CharField(max_length=100)
    facultydesig = models.CharField(max_length=100,null=True)
    facultydep = models.CharField(choices= DEPARTMENT,max_length=100,null=True)
    eventtype = models.CharField(choices=EVENTAT_TYPE,max_length=100)
    eventname = models.CharField(max_length=100,null=True)
    eventby = models.CharField(max_length=100,null=True)
    eventdesc = models.CharField(max_length=100,null=True)
    venue = models.CharField(max_length=100,null=True)
    date = models.DateField(max_length=8,default=None,null=True)

