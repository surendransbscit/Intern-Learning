from django.db import models


class ActivateHospitalPatientManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_activate = True)
    

class ActivateAndInactivate(models.QuerySet):

    def activate(self):
        return self.filter(is_activate= True)

    def inactivate(self):
        return self.filter(is_activate=False)


class hospitalactivate(models.Manager):
    
    def get_queryset(self):
        return ActivateAndInactivate(self.model, using=self._db)

    def activate(self):
        return self.get_queryset().activate()

    def inactivate(self):
        return self.get_queryset().inactivate()
    

class PatientAge(models.QuerySet):
    def child(self):
        return self.filter(patient__age__lte = 16)

    def boys(self):
        return self.filter(patient__age__gte = 17 ,patient__age__lte = 30)

    def mens(self):
        return self.filter(patient__age__gte = 31)


class PatientAgeManger(models.Manager):

    def get_queryset(self):
        return PatientAge(self.model, using=self._db)
    
    def child(self):
        return self.get_queryset().child()
    
    def boys(self):
        return self.get_queryset().boys()
    
    def mens(self):
        return self.get_queryset().mens()
    

    

    
    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    class Meta:
        db_table = 'doctor'

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(verbose_name="Category Name")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients')
    diagnosis = models.TextField()

    class Meta:
        db_table = 'patient'
        

    def __str__(self):
        return self.name
    
 
class Teachar(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'teacher'


class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'hobby'


class Student(models.Model):
    name = models.CharField(max_length=150)
    age = models.IntegerField(null=True)
    teachar = models.ForeignKey(Teachar , on_delete=models.CASCADE)
    habbice = models.ManyToManyField(Hobby)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'student'



class Hospital(models.Model):
    name = models.CharField(max_length=300)
    address = models.TextField()
    is_activate = models.BooleanField(default=True)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'hospital'


class AdmittePatientDetails(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    is_activate = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActivateHospitalPatientManager()
    active_custom = hospitalactivate()
    patientage_custom = PatientAgeManger()

    def __str__(self):
        return f"{self.patient.name} And {self.hospital.name}"
