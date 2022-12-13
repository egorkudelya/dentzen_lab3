from rest_framework import serializers
from . import models


class DentistSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Dentist
        fields = ['id', 'name', 'location', 'age', 'specialty']