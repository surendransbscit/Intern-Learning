from rest_framework import serializers
from doctorandpatientdetails.models import Doctor, Patient ,Student , Teachar, Hobby , Hospital , AdmittePatientDetails

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class HobbySerializer(serializers.ModelSerializer):

    class Meta:
        model = Hobby
        fields = '__all__'
    
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachar
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    # teachar_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Teachar.objects.all(), source='teachar', write_only=True
    # )
    # habbice_ids = serializers.PrimaryKeyRelatedField(
    #     queryset=Hobby.objects.all(), many=True, source='habbice', write_only=True
    # )

    teachar = TeacherSerializer(read_only=True)
    habbice = HobbySerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Student
        # fields = '__all__'
        # fields = ['id', 'name', 'age', 'teachar', 'habbice', 'habbice_ids', 'teachar_id']
        fields = ['id', 'name', 'age', 'teachar', 'habbice']


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id','name','address','is_activate','create_on']

class AdmittePatientDetailsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)

    class Meta:
        model = AdmittePatientDetails
        fields = ['id','patient', 'hospital', 'is_activate']


