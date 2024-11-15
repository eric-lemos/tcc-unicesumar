from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True, blank=False, null=False)
    genrer = models.CharField(max_length=20, blank=False, null=False)
    usertype = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
class Manager(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name}'
    
    def to_dict(self):
        return {
            'id': self.profile.user.pk,
            'first_name': self.profile.user.first_name,
            'last_name': self.profile.user.last_name,
            'email': self.profile.user.email,
            'genrer': self.profile.genrer,
            'cpf': self.profile.cpf,
        }

class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    crm = models.CharField(max_length=6, blank=False, null=False)
    crm_state = models.CharField(max_length=2, blank=False, null=False)
    specialization = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name}'
    
    def to_dict(self):
        return {
            'id': self.profile.user.pk,
            'first_name': self.profile.user.first_name,
            'last_name': self.profile.user.last_name,
            'email': self.profile.user.email,
            'genrer': self.profile.genrer,
            'cpf': self.profile.cpf,
            'crm': self.crm,
            'crm_state': self.crm_state,
            'specialization': self.specialization,
        }

class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.user.first_name} {self.profile.user.last_name}'
    
    def to_dict(self):
        return {
            'id': self.profile.user.pk,
            'first_name': self.profile.user.first_name,
            'last_name': self.profile.user.last_name,
            'email': self.profile.user.email,
            'genrer': self.profile.genrer,
            'cpf': self.profile.cpf,
        }
    
class Calendar(models.Model):
    protocol = models.CharField(max_length=17, unique=True, blank=False, null=False)
    doctor = models.ForeignKey(Doctor, blank=False, null=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, blank=False, null=False, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, blank=False, null=False)
    begin_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=25, blank=False, null=False)
    moderator = models.ForeignKey(Manager, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.protocol

    def to_dict(self):
        return {
            'id': self.pk,
            'protocol': self.protocol,
            'doctor': self.doctor.profile.user.pk,
            'patient': self.patient.profile.user.pk,
            'specialization': self.specialization,
            'begin_date': self.begin_date,
            'end_date': self.end_date,
        }