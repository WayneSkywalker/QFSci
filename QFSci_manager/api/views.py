from QFSci_manager.models import User, Student, Advisor, Staff, Activity, QF, Evaluate_QF_student, Evaluate_QF_activity
from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError, PermissionDenied, NotFound
from .serializers import UserSerializer, AdvisorSerializer, StudentSerializer, StaffSerializer, QFSerializer, ActivitySerializer
from .serializers import ActivityHoursSerializer, ActivityHoursYearSerializer, QFStudentGainSerializer, ActivityQFSerializer, ActivityQFStatSerializer
from .serializers import StudentQFStatSerializer, StudentParticipantStatSerializer
from .serializers import ActivityBudgetSerializer, ActivityBudgetLastSixYearsSerializer
from .serializers import EvaluateQFStudentSerializer, EvaluateQFActivitySerializer
from .serializers import UserRegisterSerializer, AdminRegisterSerializer, AdvisorRegisterSerializer, StudentRegisterSerializer, StaffRegisterSerializer, StaffAdminRegisterSerializer
from .serializers import UserEditSerializer, StudentUserEditSerializer, AdvisorEditSerializer, StudentEditSerializer, StaffEditSerializer
from .serializers import LoginSerializer, ChangePasswordSerializer
from .serializers import ActivityHoursYearSerializer_test
from django.db.models import Sum, Count, Q
from django.db.models.functions import Coalesce
from knox.models import AuthToken

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

# User Viewset
class UserViewSet(viewsets.ModelViewSet):
    
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = User.objects.all()

    serializer_class = UserSerializer

# Student Viewset
class StudentViewSet(viewsets.ModelViewSet):
    
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]

    filter_backends = (DynamicSearchFilter,)
    queryset = Student.objects.all()

    serializer_class = StudentSerializer

# Advisor Viewset
class AdvisorViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    filter_backends = (DynamicSearchFilter,)
    queryset = Advisor.objects.all()

    serializer_class = AdvisorSerializer

# Staff ViewSet
class StaffViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Staff.objects.all()
    
    serializer_class = StaffSerializer

# Activity Viewset
class ActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]

    filter_backends = (DynamicSearchFilter,)
    queryset = Activity.objects.all()

    serializer_class = ActivitySerializer

# QF Viewset
class QFViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = QF.objects.all()

    serializer_class = QFSerializer

# Evaluate QF student Viewset
class EvaluateQFStudentViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Evaluate_QF_student.objects.all()
    
    serializer_class = EvaluateQFStudentSerializer

# Evaluate QF activity Viewset
class EvaluateQFActivityViewSet(viewsets.ModelViewSet):

    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Evaluate_QF_activity.objects.all()

    serializer_class = EvaluateQFActivitySerializer

# Advisor Register API
class AdvisorRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    serializer_class = AdvisorRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        advisor = serializer.save()
        return Response({
            'advisor': AdvisorSerializer(advisor, context = self.get_serializer_context()).data
        })

# Student Register API
class StudentRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    serializer_class = StudentRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        student = serializer.save()
        return Response({
            'student': StudentSerializer(student, context = self.get_serializer_context()).data
        })

# Staff Register API
class StaffRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    serializer_class = StaffRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        staff = serializer.save()
        return Response({
            'staff': StaffSerializer(staff, context = self.get_serializer_context()).data
        })

# Admin Register API
class AdminRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    serializer_class = StaffAdminRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        admin = serializer.save()
        return Response({
            'admin (staff)': StaffSerializer(admin, context = self.get_serializer_context()).data
        })

class AdvisorEditAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Advisor.objects.all()
    serializer_class = AdvisorEditSerializer

class StudentEditAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Student.objects.all()
    serializer_class = StudentEditSerializer

class StaffEditAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        #permissions.IsAuthenticated
        #permissions.AllowAny
        permissions.IsAdminUser
    ]
    queryset = Staff.objects.all()
    serializer_class = StaffEditSerializer

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            'user': UserSerializer(user, context = self.get_serializer_context()).data,
            'token': token
        })

class ChangePasswordAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
        #permissions.IsAdminUser
    ]
    model = User
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset = None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Password is not correct.']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'new_password' : ['Change password successfully']}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ProfileAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]

    def get_serializer_class(self):
        user = self.request.user
        if user.user_type == 1:
            return StudentSerializer
        elif user.user_type ==2:
            return AdvisorSerializer
        elif user.user_type == 3:
            return StaffSerializer
        else:
            return user

    def get_object(self):
        user = self.request.user
        if user.user_type == 1:
            return Student.objects.get(user = user)
        elif user.user_type == 2:
            return Advisor.objects.get(user = user)
        elif user.user_type == 3:
            return Staff.objects.get(user = user)
        else:
            return user

class ActivityList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    filter_backends = (DynamicSearchFilter,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityDetail(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class CreateActivityAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]

    serializer_class = ActivitySerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 3:
            return serializer.save()
        raise PermissionDenied('Cannot create an activity. Because you are not a staff.')

class QFsList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    filter_backends = (DynamicSearchFilter,)
    queryset = QF.objects.all()
    serializer_class = QFSerializer

class QFDetail(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = QF.objects.all()
    serializer_class = QFSerializer

class EvaluateQFStudentAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]

    serializer_class = EvaluateQFStudentSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 1:
            student = Student.objects.get(user = user)
            serializer.save(evaluator = user, student = student)
        elif user.user_type == 2:
            if Advisor.objects.get(user = user).year_advise.filter(studentID = self.request.data['student']).exists():
                serializer.save(evaluator = user)
            raise ParseError('Cannot evaluate student qf. Because you does not advise this student.')
        raise PermissionDenied('You are a staff, so you cannot evaluate Student QF.')

class EvaluateQFActivityAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]

    serializer_class = EvaluateQFActivitySerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 1:
            student = Student.objects.get(user = user)
            if student.join_activity.filter(id = self.request.data['activity']).exists():
                activity = student.join_activity.get(id = self.request.data['activity'])
                if activity.QFs.filter(QFID = self.request.data['qf']).exists():
                    # return Response(self.request.data)
                    return serializer.save(evaluator = self.request.user)
                # raise APIException('Cannot evaluate activity qf. Because QF does not exist in this activity.')
                raise ParseError('Cannot evaluate activity qf. Because QF does not exist in this activity.')
            raise ParseError('Cannot evaluate activity qf. Because you did not join this activity.')
        elif user.user_type == 2:
            advisor = Advisor.objects.get(user = user)
            if Advisor.objects.get(user = user).advise_activity.filter(id = self.request.data['activity']).exists():
                activity = advisor.advise_activity.get(id = self.request.data['activity'])
                if activity.QFs.filter(QFID = self.request.data['qf']).exists():
                    # return Response(self.request.data)
                    return serializer.save(evaluator = self.request.user)
                raise ParseError('Cannot evaluate activity qf. Because QF does not exist in this activity.')
            raise ParseError('Cannot evaluate activity qf. Because you did not advise this activity.')
        raise PermissionDenied('You are a staff, so you cannot evaluate Activity QF.')

class ActivityHoursAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Student.objects.all()
    serializer_class = ActivityHoursSerializer

    def get_queryset(self):
        return Student.objects.annotate(activity_hours = Sum('join_activity__activity_hour'))

class ActivityHoursUserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Student.objects.all()
    serializer_class = ActivityHoursSerializer

    def get_object(self):
        user = self.request.user
        return Student.objects.annotate(activity_hours = Sum('join_activity__activity_hour')).get(user = user)

class ActivityHoursYearsAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Student.objects.all()
    serializer_class = ActivityHoursYearSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        if Student.objects.filter(studentID = pk).exists():
            student = Student.objects.get(pk = pk)
            return student.join_activity.values('year').annotate(activity_hours_gain = Sum('activity_hour'),\
                activity_hours_need =  25 - Sum('activity_hour')).order_by()
        raise NotFound('This student does not exist.')

class ActivityHoursYearsUserAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Student.objects.all()
    serializer_class = ActivityHoursYearSerializer

    def get_queryset(self):
        user = self.request.user
        if Student.objects.filter(user = user).exists():
            student = Student.objects.get(user = user)
            return student.join_activity.values('year').annotate(activity_hours_gain = Sum('activity_hour'),\
                activity_hours_need =  25 - Sum('activity_hour')).order_by()
        raise NotFound('This student does not exist.')

class ActivityHoursYearUserAPI_test(generics.ListAPIView): ######################################
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = Student.objects.all()
    serializer_class = ActivityHoursYearSerializer_test

    def get_object(self):
        user = self.request.user
        if Student.objects.filter(user = user).exists():
            student = Student.objects.get(user = user)
            # studentID = student.studentID
            # year_code = int(studentID[:2])
            # year_1 = year_code + 2500
            # year_2 = year_code + 2501
            # year_3 = year_code + 2502
            # year_4 = year_code + 2503
            return Student.objects.annotate(activity_hours_year_1 = Coalesce(Sum('join_activity__activity_hour', filter = Q(join_activity__year = 2560)),0),\
                activity_hours_year_2 = Coalesce(Sum('join_activity__activity_hour', filter = Q(join_activity__year = 2561)),0),\
                activity_hours_year_3 = Coalesce(Sum('join_activity__activity_hour', filter = Q(join_activity__year = 2562)),0),\
                activity_hours_year_4 = Coalesce(Sum('join_activity__activity_hour', filter = Q(join_activity__year = 2563)),0)).get(user = user)
        raise NotFound('This student does not exist.')

class QFStudentGainAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = QF.objects.all()
    serializer_class = QFStudentGainSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return QF.objects.annotate(gain = Count('activity_qf',filter = Q(activity_qf__joined_students__studentID = pk)))\
            .values('QF_name','gain')

class QFStudentGainUserAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = QF.objects.all()
    serializer_class = QFStudentGainSerializer

    def get_queryset(self):
        user = self.request.user
        return QF.objects.annotate(gain = Count('activity_qf',filter = Q(activity_qf__joined_students__user = user)))\
            .values('QF_name','gain')

class QFStudentYearGainAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = QF.objects.all()
    serializer_class = QFStudentGainSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        year = self.kwargs['year']
        return  QF.objects.annotate(gain = Count('activity_qf',filter = Q(activity_qf__joined_students__studentID = pk)\
            & Q(activity_qf__year = year))).values('QF_name','gain')

class QFStudentYearGainUserAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    queryset = QF.objects.all()
    serializer_class = QFStudentGainSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.kwargs['year']
        return  QF.objects.annotate(gain = Count('activity_qf',filter = Q(activity_qf__joined_students__user = user)\
            & Q(activity_qf__year = year))).values('QF_name','gain')

class AdvisedStudentsList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Advisor.objects.get(user = self.request.user).year_advise.all() # ERROR_500 if doesn't match any query

class AdvisedStudentProfile(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Advisor.objects.get(user = self.request.user).year_advise.all() # ERROR_500 if doesn't match any query

class ActivityBudgetYearAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivityBudgetSerializer

    def get_object(self):
        user = self.request.user
        year = self.kwargs['year']
        if user.user_type == 3:
            return Activity.objects.filter(year = year).aggregate(Sum('budget'))
        raise PermissionDenied('Cannot access the information. You are not a staff.')
        
class MostBudgetUsedActivities(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        year = self.kwargs['year']
        user = self.request.user
        if user.user_type == 3:
            return Activity.objects.filter(year = year).order_by('-budget')[:5]
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class ActivityBudgetLastSixYearsAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivityBudgetLastSixYearsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 3:
            return Activity.objects.values('year').annotate(budget_sum = Sum('budget')).order_by('-year')[:6]
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class QFsInOneActivityAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivityQFSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        if Activity.objects.filter(id = pk).exists():
            return Activity.objects.get(pk = pk).QFs.all()
        raise NotFound('This activity does not exist.')

class QFGotActivityList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        QFID = self.kwargs['QFID']
        return Activity.objects.filter(QFs__QFID = QFID)

class QFGotActivityYearList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivitySerializer

    def get_queryset(self):
        QFID = self.kwargs['QFID']
        year = self.kwargs['year']
        return Activity.objects.filter(QFs__QFID = QFID, year = year)

class ActivityQFStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivityQFStatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 3:
            return QF.objects.annotate(activity_count = Count('activity_qf')).values('QF_name','activity_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class ActivityQFYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = ActivityQFStatSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.kwargs['year']
        if user.user_type == 3:
            return QF.objects.annotate(activity_count = Count('activity_qf', filter = Q(activity_qf__year = year)))\
                .values('QF_name','activity_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

# **** all of these following stat API are one-year-stat queries ****

class StudentQFAllStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    filter_backends = (DynamicSearchFilter,)
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.kwargs['year']
        if user.user_type == 3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students', distinct = True,\
                filter = Q(activity_qf__year = year))).values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentQFFacultyStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        faculties = {
            'science': 'วิทยาศาสตร์',
            'engineering': 'วิศวกรรมศาสตร์'
        }
        user = self.request.user
        year = self.kwargs['year']
        faculty = faculties[self.kwargs['faculty']]
        if user.user_type == 3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students', distinct = True,\
                filter = Q(activity_qf__joined_students__faculty = faculty) & Q(activity_qf__year = year)))\
                .values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentQFDepartmentStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        departments = {
            'MTH': 'คณิตศาสตร์',
            'PHY': 'ฟิสิกส์',
            'CHM': 'เคมี',
            'MIC': 'จุลชีววิทยา'
        }
        user = self.request.user
        year = self.kwargs['year']
        department = departments[self.kwargs['department']]
        if user.user_type ==3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students',\
                distinct = True, filter = Q(activity_qf__joined_students__department = department) & Q(activity_qf__year = year)))\
                .values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentQFYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        user = self.request.user
        year = self.kwargs['year']
        year_of_study = self.kwargs['year_of_study']
        if user.user_type ==3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students', distinct = True, \
                filter = Q(activity_qf__joined_students__year_of_study = year_of_study) & Q(activity_qf__year = year)))\
                .values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentQFDepartmentYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        departments = {
            'MTH': 'คณิตศาสตร์',
            'PHY': 'ฟิสิกส์',
            'CHM': 'เคมี',
            'MIC': 'จุลชีววิทยา'
        }
        user = self.request.user
        year = self.kwargs['year']
        year_of_study = self.kwargs['year_of_study']
        department = departments[self.kwargs['department']]
        if user.user_type == 3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students', distinct = True, \
                filter = Q(activity_qf__joined_students__department = department) & Q(activity_qf__year = year) \
                & Q(activity_qf__joined_students__year_of_study = year_of_study))).values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentQFFacultyYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentQFStatSerializer

    def get_queryset(self):
        faculties = {
            'science': 'วิทยาศาสตร์',
            'engineering': 'วิศวกรรมศาสตร์'
        }
        user = self.request.user
        year = self.kwargs['year']
        year_of_study = self.kwargs['year_of_study']
        faculty = faculties[self.kwargs['faculty']]
        if user.user_type == 3:
            return QF.objects.annotate(student_count = Count('activity_qf__joined_students', distinct = True, \
                filter = Q(activity_qf__joined_students__faculty = faculty) & Q(activity_qf__year = year) & \
                Q(activity_qf__joined_students__year_of_study = year_of_study))).values('QF_name','student_count')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class AdvisedStudentParticipationStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 2:
            return Student.objects.filter(year_advisor__user = user)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not an advisor.')

class StudentParticipantAllStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 3:
            return Student.objects.annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentParticipantFacultyStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        faculties = {
            'science': 'วิทยาศาสตร์',
            'engineering': 'วิศวกรรมศาสตร์'
        }
        user = self.request.user
        faculty = faculties[self.kwargs['faculty']]
        if user.user_type == 3:
            return Student.objects.filter(faculty = faculty)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentParticipationDepartmentStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        departments = {
            'MTH': 'คณิตศาสตร์',
            'PHY': 'ฟิสิกส์',
            'CHM': 'เคมี',
            'MIC': 'จุลชีววิทยา'
        }
        user = self.request.user
        department = departments[self.kwargs['department']]
        if user.user_type == 3:
            return Student.objects.filter(department = department)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentParticipantYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        user = self.request.user
        year_of_study = self.kwargs['year_of_study']
        if user.user_type == 3:
            return Student.objects.filter(year_of_study = year_of_study)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentParticipantDepartmentYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        departments = {
            'MTH': 'คณิตศาสตร์',
            'PHY': 'ฟิสิกส์',
            'CHM': 'เคมี',
            'MIC': 'จุลชีววิทยา'
        }
        user = self.request.user
        year_of_study = self.kwargs['year_of_study']
        department = departments[self.kwargs['department']]
        if user.user_type == 3:
            return Student.objects.filter(year_of_study = year_of_study, department = department)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')

class StudentParticipantFacultyYearStatAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
        #permissions.AllowAny
    ]
    serializer_class = StudentParticipantStatSerializer

    def get_queryset(self):
        faculties = {
            'science': 'วิทยาศาสตร์',
            'engineering': 'วิศวกรรมศาสตร์'
        }
        user = self.request.user
        year_of_study = self.kwargs['year_of_study']
        faculty = faculties[self.kwargs['faculty']]
        if user.user_type == 3:
            return Student.objects.filter(year_of_study = year_of_study, faculty = faculty)\
                .annotate(activity_hour_sum = Sum('join_activity__activity_hour', distinct = True),\
                qf_1 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF01')),\
                qf_2 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF02')),\
                qf_3 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF03')),\
                qf_4 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF04')),\
                qf_5 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF05')),\
                qf_6 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF06')),\
                qf_7 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF07')),\
                qf_8 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF08')),\
                qf_9 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF09')),\
                qf_10 = Count('join_activity', filter = Q(join_activity__QFs__QFID = 'QF10')))\
                .values('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10')
        raise PermissionDenied('Cannot access the information. You are not a staff.')