from django.utils.timezone import now
from django.db import models


class Dentist(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(max_length=255, blank=True, null=True)
    specialty = models.TextField(max_length=255, blank=True, null=True)
    age = models.IntegerField(default=0)

    class Meta:
        db_table = 'dentists'


class DentalClinic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    staff = models.IntegerField(default=0)
    location = models.TextField(max_length=255, blank=True, null=True)
    opens = models.TimeField(default='8:00:00')
    closes = models.TimeField(default='20:00:00')

    class Meta:
        db_table = 'clinics'


class DentistClinicContract(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=now)
    clinic = models.ForeignKey(DentalClinic, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['clinic', 'dentist']
        db_table = 'dentist_clinic_contracts'


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    years_on_market = models.IntegerField(default=0)
    location = models.TextField(max_length=255, blank=True, null=True)


class SupplierClinicContract(models.Model):
    clinic = models.ForeignKey(DentalClinic, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class BaseSupplierProduct(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(blank=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Drug(BaseSupplierProduct):
    volume = models.FloatField(default=0.0)
    age_restriction = models.IntegerField(default=0)


class Instrument(BaseSupplierProduct):
    weight = models.FloatField(default=0.0)
    is_reusable = models.BooleanField(default=False)


class Disease(models.Model):
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)


class Diagnosis(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(max_length=255, blank=True, null=True)
    date_time = models.DateTimeField(blank=True, default=now)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
