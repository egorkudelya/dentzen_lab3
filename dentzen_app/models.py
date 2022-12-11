from django.db import models


class DentalClinic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    staff = models.IntegerField(default=0)
    location = models.TextField(max_length=255, blank=True, null=True)
    opens = models.TimeField(default='8:00:00')
    closes = models.TimeField(default='20:00:00')


class Dentist(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(max_length=255, blank=True, null=True)
    specialty = models.TextField(max_length=255, blank=True, null=True)
    age = models.IntegerField(default=0)


class DentistClinicContract(models.Model):
    clinic = models.ForeignKey(DentalClinic, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=255, blank=True, null=True)
    years_on_market = models.IntegerField(default=0)
    location = models.TextField(max_length=255, blank=True, null=True)


class SupplierClinicContract(models.Model):
    clinic = models.ForeignKey(DentalClinic, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)


class Drug(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(blank=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    supplier = models.ManyToManyField(Supplier)


class Instrument(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(blank=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    supplier = models.ManyToManyField(Supplier)


class Appointment(models.Model):
    pass


class Patient(models.Model):
    pass


class Diagnosis(models.Model):
    pass


class Disease(models.Model):
    pass
