from django.contrib import admin
from .models import User, Student, Advisor, Staff, Activity, QF, Evaluate_QF_student, Evaluate_QF_activity

admin.site.site_header = 'QFSci Admin'
admin.site.site_title = 'QFSci Admin'
admin.site.index_title = 'QFSci Administration site'

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Staff)
admin.site.register(Activity)
admin.site.register(QF)
admin.site.register(Evaluate_QF_student)
admin.site.register(Evaluate_QF_activity)