from django.urls import path, include
from .views import StudentRegisterAPI, AdvisorRegisterAPI, StaffRegisterAPI, AdminRegisterAPI
from .views import LoginAPI, UserAPI, ProfileAPI, StudentEditAPI, AdvisorEditAPI, StaffEditAPI
from .views import ActivityList, ActivityDetail, CreateActivityAPI, ActivityHoursAPI, ActivityHoursYearsAPI
from .views import QFsInOneActivityAPI, QFGotActivityList, QFGotActivityYearList, ActivityQFStatAPI, ActivityQFYearStatAPI
from .views import ActivityBudgetYearAPI, MostBudgetUsedActivities, ActivityBudgetLastSixYearsAPI
from .views import AdvisedStudentsList, AdvisedStudentProfile, AdvisedStudentParticipationStatAPI
from .views import QFsList, QFDetail, QFStudentGainAPI, QFStudentYearGainAPI
from .views import StudentQFAllStatAPI, StudentQFFacultyStatAPI, StudentQFDepartmentStatAPI, StudentQFYearStatAPI
from .views import StudentQFDepartmentYearStatAPI, StudentQFFacultyYearStatAPI, StudentParticipantAllStatAPI
from .views import StudentParticipantFacultyStatAPI, StudentParticipationDepartmentStatAPI, StudentParticipantYearStatAPI
from .views import StudentParticipantDepartmentYearStatAPI, StudentParticipantFacultyYearStatAPI
from .views import EvaluateQFStudentAPI, EvaluateQFActivityAPI
from .views import ChangePasswordAPI, ActivityHoursUserAPI, ActivityHoursYearsUserAPI, QFStudentGainUserAPI, QFStudentYearGainUserAPI
from .views import ActivityHoursYearUserAPI_2, ActivityHoursYearsAPI_2
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name = 'knox_logout'),
    path('api/admin/students/register', StudentRegisterAPI.as_view()),
    path('api/admin/advisors/register', AdvisorRegisterAPI.as_view()),
    path('api/admin/staffs/register', StaffRegisterAPI.as_view()),
    path('api/admin/admins/register', AdminRegisterAPI.as_view()),
    path('api/admin/students/edit/<str:pk>', StudentEditAPI.as_view()),
    path('api/admin/advisors/edit/<str:pk>', AdvisorEditAPI.as_view()),
    path('api/admin/staffs/edit/<str:pk>', StaffEditAPI.as_view()),
    path('api/profile', ProfileAPI.as_view()),
    path('api/profile/change-password', ChangePasswordAPI.as_view()),
    path('api/student/activity-hours/<str:pk>', ActivityHoursAPI.as_view()),
    path('api/student/activity-hours', ActivityHoursUserAPI.as_view()),
    path('api/student/activity-hours-per-year/<str:pk>', ActivityHoursYearsAPI.as_view()),
    path('api/student/activity-hours-per-year', ActivityHoursYearsUserAPI.as_view()),
    path('api/student/activity-hours-per-year-2', ActivityHoursYearUserAPI_2.as_view()),
    path('api/student/activity-hours-per-year-2/<str:pk>', ActivityHoursYearsAPI_2.as_view()),
    path('api/student/QF/<str:pk>', QFStudentGainAPI.as_view()),
    path('api/student/QF', QFStudentGainUserAPI.as_view()),
    path('api/student/QF/<str:pk>/<int:year>', QFStudentYearGainAPI.as_view()),
    path('api/student/QF-year/<int:year>', QFStudentYearGainUserAPI.as_view()),
    path('api/advisor/advised-students', AdvisedStudentsList.as_view()),
    path('api/advisor/advised-students/<str:pk>', AdvisedStudentProfile.as_view()),
    path('api/advisor/advised-students-participation-stat', AdvisedStudentParticipationStatAPI.as_view()),
    path('api/evaluate-student-qf', EvaluateQFStudentAPI.as_view()),
    path('api/evaluate-activity-qf', EvaluateQFActivityAPI.as_view()),
    path('api/staff/activity-budget-in-year/<int:year>', ActivityBudgetYearAPI.as_view()),
    path('api/staff/5-most-used-budget-activities-of-the-year/<int:year>', MostBudgetUsedActivities.as_view()),
    path('api/staff/activity-budget-in-last-6-year', ActivityBudgetLastSixYearsAPI.as_view()),
    path('api/staff/activity-qf-stat', ActivityQFStatAPI.as_view()),
    path('api/staff/activity-qf-stat/<int:year>', ActivityQFYearStatAPI.as_view()),
    path('api/staff/student-qf-stat/all/<int:year>', StudentQFAllStatAPI.as_view()),
    path('api/staff/student-qf-stat/faculty/<str:faculty>/<int:year>', StudentQFFacultyStatAPI.as_view()), # faculty --> science (วิทยาศาสตร์), engineering (วิศวกรรมศาสตร์)
    path('api/staff/student-qf-stat/department/<str:department>/<int:year>', StudentQFDepartmentStatAPI.as_view()), # department --> MTH (คณิตศาสตร์), PHY (ฟิสิกส์), CHM (เคมี), MIC (จุลชีววิทยา)
    path('api/staff/student-qf-stat/year-of-study/<int:year_of_study>/<int:year>', StudentQFYearStatAPI.as_view()),
    path('api/staff/student-qf-stat/year-of-study+department/<int:year_of_study>/<str:department>/<int:year>', StudentQFDepartmentYearStatAPI.as_view()),
    path('api/staff/student-qf-stat/year-of-study+faculty/<int:year_of_study>/<str:faculty>/<int:year>', StudentQFFacultyYearStatAPI.as_view()),
    path('api/staff/student-participant-stat/all', StudentParticipantAllStatAPI.as_view()),
    path('api/staff/student-participant-stat/faculty/<str:faculty>', StudentParticipantFacultyStatAPI.as_view()),
    path('api/staff/student-participant-stat/department/<str:department>', StudentParticipationDepartmentStatAPI.as_view()),
    path('api/staff/student-participant-stat/year-of-study/<int:year_of_study>', StudentParticipantYearStatAPI.as_view()),
    path('api/staff/student-participant-stat/year-of-study+department/<int:year_of_study>/<str:department>', StudentParticipantDepartmentYearStatAPI.as_view()),
    path('api/staff/student-participant-stat/year-of-study+faculty/<int:year_of_study>/<str:faculty>', StudentParticipantFacultyYearStatAPI.as_view()),
    path('api/activity', ActivityList.as_view()),
    path('api/activity/<int:pk>', ActivityDetail.as_view()),
    path('api/activity/<int:pk>/QFs', QFsInOneActivityAPI.as_view()),
    path('api/activity/create', CreateActivityAPI.as_view()),
    path('api/activity/got-QF/<str:QFID>', QFGotActivityList.as_view()),
    path('api/activity/got-QF/<str:QFID>/<int:year>', QFGotActivityYearList.as_view()),
    path('api/QF', QFsList.as_view()),
    path('api/QF/<str:pk>', QFDetail.as_view()),
]