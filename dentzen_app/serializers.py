from rest_framework import serializers
from . import models


class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dentist
        fields = ['id', 'name', 'location', 'age', 'specialty']


class DentalClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DentalClinic
        fields = ['id', 'name', 'location', 'description', 'staff', 'opens', 'closes', 'dentists']
        depth = 1


class DentistClinicContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DentistClinicContract
        fields = ['id', 'name', 'date', 'clinic', 'dentist']
        depth = 1
