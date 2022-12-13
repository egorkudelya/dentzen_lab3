from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response


class DentistView(APIView):

    def get(self, request, **kwargs):
        query = 'SELECT * FROM dentists'
        if 'id' in kwargs:
            query += ' WHERE id=(%s)' % kwargs['id']

        dentists = models.Dentist.objects.raw(query)
        serialized_dentists = serializers.DentistSerializer(dentists, many=True)
        return Response(serialized_dentists.data)


    def post(self, request):
        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())

        query = f"INSERT INTO dentists (%s) VALUES (%s) RETURNING *;" % (columns, values)

        queryset = models.Dentist.objects.raw(query)
        data = [serializers.DentistSerializer(model).data for model in queryset]

        return Response(data)
