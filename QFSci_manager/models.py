from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Student'),
        (2, 'Advisor'),
        (3, 'Staff')
    )

    # firstname and lastname fields are automatically added in Abstractuser.

    # types of user
    user_type = models.PositiveSmallIntegerField(choices = USER_TYPE_CHOICES)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Advisor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    ## advisor's information
    advisorID = models.CharField(max_length = 15, unique = True, primary_key = True)

    # type choices of academic rank
    ACADENIC_RANK_TYPE = (
        ('ศ. ดร.','ศาตราจารย์ดอกเตอร์'),
        ('ศ.','ศาตราจารย์'),
        ('รศ. ดร.','รองศาตราจารย์ดอกเตอร์'),
        ('รศ.','รองศาตราจารย์'),
        ('ผศ. ดร.','ผู้ช่วยศาตราจารย์ดอกเตอร์'),
        ('ผศ.','ผู้ช่วยศาตราจารย์'),
        ('ดร.', 'ดอกเตอร์'),
        ('อ.', 'อาจารย์'),
    )
    academic_rank = models.CharField(max_length = 8, choices = ACADENIC_RANK_TYPE)
    faculty = models.CharField(max_length = 60)
    department = models.CharField(max_length = 80)

    class Meta:
        ordering = ['-academic_rank']

    # display advisor's name
    def __str__(self):
        return '%s%s %s' % (self.academic_rank, self.user.first_name, self.user.last_name)


### student model

class Student(models.Model):
    ## student's account
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    ## student's information
    studentID = models.CharField(max_length = 11, unique = True, primary_key = True)
    # year of study
    YEAR_CHOICES = (
        (1, 'Freshmen'),
        (2, 'Sophomore'),
        (3, 'Junior'),
        (4, 'Senior'),
        (5, '5th-year'),
        (6, '6th-year'),
        (7, '7th-year'),
        (8, '8th-year'),
        (9, 'Graduate')
    )
    year_of_study = models.PositiveSmallIntegerField(choices = YEAR_CHOICES)
    degree_of_study = models.CharField(max_length = 80)
    faculty = models.CharField(max_length = 60)
    department = models.CharField(max_length = 80)
    field_of_study = models.CharField(max_length = 80)

    # year advisor
    year_advisor = models.ForeignKey(Advisor, related_name = 'year_advise', on_delete = models.CASCADE)

    class Meta:
        ordering = ['studentID']

    # display student's name
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
    # display student's ID
    def get_student_ID(self):
        return self.studentID

### staff model

class Staff(models.Model):
    ## Staff's account
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    is_admin = models.BooleanField(default = False) # Is staff also 'admin' ? True : False

    ## staff's information
    staffID = models.CharField(max_length = 15, unique = True, primary_key = True)
    working_unit = models.CharField(max_length = 60)

    # display staff's name
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


### QF model

class QF(models.Model):
    ## QF's information
    QFID = models.CharField(max_length = 4, unique = True, primary_key = True)
    QF_name = models.CharField(max_length = 60, unique = True)
    QF_description = models.CharField(max_length = 300)

    # display QF's name
    def __str__(self):
        return self.QF_name


### activity model

class Activity(models.Model):
    ## activity's information
    # activityID = models.CharField(max_length = 15, unique = True, primary_key = True)
    activity_name = models.CharField(max_length = 100, unique = True)

    activity_type = models.CharField(max_length = 100)

    year = models.PositiveSmallIntegerField() # academic year
    activity_unit = models.CharField(max_length = 120) # working unit, which create activity.

    #activity_advisor = models.ManyToManyField(Advisor, through = 'Activity_advised') # activity advisor
    activity_advisor = models.ManyToManyField(Advisor, related_name = 'advise_activity')

    # place, which activity is organized
    in_university = models.BooleanField() # Place is in university ? True : False
    place = models.CharField(max_length = 200)

    # student joined
    #joined_students = models.ManyToManyField(Student, through = 'Join_activity')
    joined_students = models.ManyToManyField(Student, related_name = 'join_activity')

    target_participants = models.PositiveIntegerField()
    predicted_participants = models.PositiveIntegerField()
    actual_participants = models.PositiveIntegerField()

    activity_date_begin = models.DateField() # date, which activity begin
    activity_date_end = models.DateField() # date, which activity end
    
    project_date_begin = models.DateField() # first date, which project is organized.
    project_date_end = models.DateField() # last date, which project is organized.
    
    activity_hour = models.PositiveSmallIntegerField()

    # QF in activity
    #QFs = models.ManyToManyField(QF)
    QFs = models.ManyToManyField(QF, related_name = 'activity_qf')

    activity_leader_studentID = models.CharField(max_length = 11, blank = True)
    activity_leader_firstname = models.CharField(max_length = 40)
    activity_leader_lastname = models.CharField(max_length = 70)

    budget = models.FloatField()

    class Meta:
        ordering = ['-year','activity_date_begin']

    # display activity's name
    def __str__(self):
        return self.activity_name


### student's QF evaluation relationship model

class Evaluate_QF_student(models.Model):
    evaluator = models.ForeignKey(User, on_delete = models.CASCADE)
    qf = models.ForeignKey(QF, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    date_evaluated = models.DateTimeField(auto_now_add = True)


### activity's QF evaluation relationship model

class Evaluate_QF_activity(models.Model):
    evaluator = models.ForeignKey(User, on_delete = models.CASCADE)
    qf = models.ForeignKey(QF, on_delete = models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete = models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    date_evaluated = models.DateTimeField(auto_now_add = True)