from rest_framework import routers
from .views import UserViewSet, AdvisorViewSet, StudentViewSet, StaffViewSet, QFViewSet, ActivityViewSet, EvaluateQFStudentViewSet, EvaluateQFActivityViewSet

router = routers.DefaultRouter()

router.register('api/admin/users', UserViewSet, 'users')
router.register('api/admin/students', StudentViewSet, 'students')
router.register('api/admin/advisors', AdvisorViewSet, 'advisors')
router.register('api/admin/staffs', StaffViewSet, 'staffs')
router.register('api/admin/activities', ActivityViewSet, 'activities')
router.register('api/admin/QFs', QFViewSet, 'QFs')
router.register('api/admin/student-QF-evaluations', EvaluateQFStudentViewSet, 'student-QF-evaluations')
router.register('api/admin/activity-QF-evaluations', EvaluateQFActivityViewSet, 'activity-QF-evaluations')

urlpatterns = router.urls