from rest_framework import serializers
from django.contrib.auth import authenticate
from QFSci_manager.models import User, Student, Advisor, Staff, Activity, QF, Evaluate_QF_student, Evaluate_QF_activity
from knox.models import AuthToken

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','user_type')

# User Serializer for registeration
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','user_type')
        extra_kwarg = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = User.objects.create_user(validated_data['username'], validated_data['password'], validated_data['first_name'], validated_data['last_name'], validated_data['user_type'])
        user = User.objects.create_user(username = validated_data['username'], password = validated_data['password'], first_name =  validated_data['first_name'], last_name = validated_data['last_name'], user_type = validated_data['user_type'])
        return user

# User Serializer for admin registeration
class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','user_type')
        extra_kwarg = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(username = validated_data['username'], password = validated_data['password'], first_name =  validated_data['first_name'], last_name = validated_data['last_name'], user_type = validated_data['user_type'])
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            if not AuthToken.objects.filter(user = user).exists():
                return user
            raise serializers.ValidationError("This user is already logged in.")
        raise serializers.ValidationError("Incorrect Credentials")

# User Serializer for editing advisor and staff information
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name')

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

# class PasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('password')

# User Serializer for editing student's information
class StudentUserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name')
        read_only_fields = ('username',)

# Advisor Serializer
class AdvisorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    year_advise = serializers.StringRelatedField(many = True)
    advise_activity = serializers.StringRelatedField(many = True)

    class Meta:
        model = Advisor
        fields = '__all__'

# Advisor Serializer for registeration
class AdvisorRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Advisor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegisterSerializer(data = user_data)
        user_serializer.is_valid(raise_exception = True)
        validated_data['user'] = user_serializer.save()
        instance = super().create(validated_data)
        return instance

# Advisor Serializer for editing advisor's information
class AdvisorEditSerializer(serializers.ModelSerializer):
    user = UserEditSerializer()

    class Meta:
        model = Advisor
        fields = ('user','academic_rank', 'faculty', 'department')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_edited = instance.user
        instance.academic_rank = validated_data.get('academic_rank', instance.academic_rank)
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        user_edited.username = user_data.get('username', user_edited.username)
        user_edited.password = user_data.get('password', user_edited.password)
        user_edited.first_name = user_data.get('first_name', user_edited.first_name)
        user_edited.last_name = user_data.get('last_name', user_edited.last_name)
        user_edited.save()
        return instance

# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    join_activity = serializers.StringRelatedField(many = True)

    class Meta:
        model = Student
        fields = '__all__'

# Student Serializer for registeration
class StudentRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegisterSerializer(data = user_data)
        user_serializer.is_valid(raise_exception = True)
        validated_data['user'] = user_serializer.save()
        instance = super().create(validated_data)
        return instance

# Student Serializer for editing student's information
class StudentEditSerializer(serializers.ModelSerializer):
    user = StudentUserEditSerializer()

    class Meta:
        model = Student
        fields = ('user', 'year_of_study', 'degree_of_study', 'faculty', 'department', 'field_of_study', 'year_advisor')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_edited = instance.user
        instance.year_of_study = validated_data.get('year_of_study', instance.year_of_study)
        instance.degree_of_study = validated_data.get('degree_of_study', instance.degree_of_study)
        instance.faculty = validated_data.get('faculty', instance.faculty)
        instance.department = validated_data.get('department', instance.department)
        instance.field_of_study = validated_data.get('field_of_study', instance.field_of_study)
        instance.year_advisor = validated_data.get('year_advisor', instance.year_advisor)
        instance.save()
        user_edited.password = user_data.get('password', user_edited.password)
        user_edited.first_name = user_data.get('first_name', user_edited.first_name)
        user_edited.last_name = user_data.get('last_name', user_edited.last_name)
        user_edited.save()
        return instance

# Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = '__all__'

# Staff Serializer for registeration
class StaffRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()

    class Meta:
        model = Staff
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserRegisterSerializer(data = user_data)
        user_serializer.is_valid(raise_exception = True)
        validated_data['user'] = user_serializer.save()
        instance = super().create(validated_data)
        return instance

class StaffAdminRegisterSerializer(serializers.ModelSerializer):
    user = AdminRegisterSerializer()

    class Meta:
        model = Staff
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = AdminRegisterSerializer(data = user_data)
        user_serializer.is_valid(raise_exception = True)
        validated_data['user'] = user_serializer.save()
        instance = super().create(validated_data)
        return instance

class StaffEditSerializer(serializers.ModelSerializer):
    user = UserEditSerializer()

    class Meta:
        model = Staff
        fields = fields = ('user', 'is_admin', 'working_unit')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_edited = instance.user
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.working_unit = validated_data.get('working_unit', instance.working_unit)
        instance.save()
        user_edited.username = user_data.get('username', user_edited.username)
        user_edited.password = user_data.get('password', user_edited.password)
        user_edited.first_name = user_data.get('first_name', user_edited.first_name)
        user_edited.last_name = user_data.get('last_name', user_edited.last_name)
        user_edited.save()
        return instance

# QF Serializer
class QFSerializer(serializers.ModelSerializer):
    activity_qf = serializers.StringRelatedField(many = True)

    class Meta:
        model = QF
        fields = '__all__'

# Activity Serializer
class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'

# Student QF evaluation Serializer
class EvaluateQFStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluate_QF_student
        exclude = ('id',)

# Activity QF evaluation Serializer
class EvaluateQFActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Evaluate_QF_activity
        exclude = ('id',)

# Activity hours Serializer
class ActivityHoursSerializer(serializers.ModelSerializer):
    activity_hours = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ('activity_hours',)

# Activity hours per year Serializer
class ActivityHoursYearSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    activity_hours_gain = serializers.IntegerField()
    activity_hours_need = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ('year', 'activity_hours_gain','activity_hours_need',)

# class ActivityHoursYearSerializer_test(serializers.ModelSerializer): ##############################################
#     activity_hours_year_1 = serializers.IntegerField()
#     activity_hours_year_2 = serializers.IntegerField()
#     activity_hours_year_3 = serializers.IntegerField()
#     activity_hours_year_4 = serializers.IntegerField()

#     class Meta:
#         model = Student
#         fields = ('activity_hours_year_1','activity_hours_year_2','activity_hours_year_3','activity_hours_year_4',)

class QFStudentGainSerializer(serializers.ModelSerializer):
    gain = serializers.IntegerField()

    class Meta:
        model = QF
        fields = ('QF_name','gain',)

class ActivityQFSerializer(serializers.ModelSerializer):
    class Meta:
        model = QF
        fields = ('QF_name', 'QF_description',)

class ActivityBudgetSerializer(serializers.ModelSerializer):
    budget__sum = serializers.IntegerField()

    class Meta:
        model = Activity
        fields = ('budget__sum',)

class ActivityBudgetLastSixYearsSerializer(serializers.ModelSerializer):
    budget_sum = serializers.IntegerField()

    class Meta:
        model = Activity
        fields = ('year','budget_sum',)

class ActivityQFStatSerializer(serializers.ModelSerializer):
    activity_count = serializers.IntegerField()
    
    class Meta:
        model = QF
        fields = ('QF_name','activity_count',)
        
class StudentQFStatSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField()

    class Meta:
        model = QF
        fields = ('QF_name','student_count',)

class StudentParticipantStatSerializer(serializers.ModelSerializer):
    user__first_name = serializers.CharField()
    user__last_name = serializers.CharField()
    activity_hour_sum = serializers.IntegerField()
    qf_1 = serializers.IntegerField()
    qf_2 = serializers.IntegerField()
    qf_3 = serializers.IntegerField()
    qf_4 = serializers.IntegerField()
    qf_5 = serializers.IntegerField()
    qf_6 = serializers.IntegerField()
    qf_7 = serializers.IntegerField()
    qf_8 = serializers.IntegerField()
    qf_9 = serializers.IntegerField()
    qf_10 = serializers.IntegerField()

    class Meta:
        model = Student
        fields = ('studentID','user__first_name','user__last_name','activity_hour_sum','qf_1','qf_2','qf_3','qf_4','qf_5','qf_6','qf_7','qf_8','qf_9','qf_10',)
