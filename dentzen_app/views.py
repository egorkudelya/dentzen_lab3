from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class DentistShowView(APIView):

    def get(self, request, **kwargs):
        query = 'SELECT * FROM dentists WHERE id=%s' % kwargs['id']
        dentists = models.Dentist.objects.raw(query)
        serialized_dentists = serializers.DentistSerializer(dentists, many=True)
        return Response(serialized_dentists.data, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        retrieve_query = 'SELECT * FROM dentists WHERE id=%s' % kwargs['id']
        queryset = models.Dentist.objects.raw(retrieve_query)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        old_data = serializers.DentistSerializer(queryset[0]).data

        updated_data = {k: request.data[k] for k in request.data if
                        old_data.get(k, not request.data[k]) != request.data[k]}
        upd_str = ', '.join(
            f"{key} = '{val}'" if isinstance(val, str) else f"{key} = {val}" for key, val in updated_data.items()
        )

        update_query = f'UPDATE dentists SET %s WHERE id=%s RETURNING *;' % (upd_str, kwargs['id'])
        queryset = models.Dentist.objects.raw(update_query)
        serialized_data = serializers.DentistSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        delete_query = 'DELETE FROM dentists WHERE id=%s' % kwargs['id']
        with connection.cursor() as cursor:
            cursor.execute(delete_query)

        return Response({"message": f"Dentist with id {kwargs['id']} has been deleted"}, status=status.HTTP_200_OK)


class DentistIndexView(APIView):

    def get(self, request):
        query = 'SELECT * FROM dentists'
        dentists = models.Dentist.objects.raw(query)
        serialized_dentists = serializers.DentistSerializer(dentists, many=True)
        return Response(serialized_dentists.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not bool(request.data):
            return Response({"message": f"Empty body provided"}, status=status.HTTP_400_BAD_REQUEST)

        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())
        query = f"INSERT INTO dentists (%s) VALUES (%s) RETURNING *;" % (columns, values)
        queryset = models.Dentist.objects.raw(query)
        serialized_data = serializers.DentistSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class ClinicShowView(APIView):

    def get(self, request, **kwargs):
        query = """SELECT DISTINCT c.*, d.*
                   FROM clinics c
                   LEFT JOIN dentist_clinic_contracts dcc on dcc.clinic_id = c.id
                   LEFT JOIN dentists d on d.id = dcc.dentist_id
                   WHERE c.id =%s""" % kwargs['id']

        clinics = models.DentalClinic.objects.raw(query)
        serialized_clinics = serializers.DentalClinicSerializer(clinics, many=True)
        return Response(serialized_clinics.data, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        retrieve_query = 'SELECT * FROM clinics WHERE id=%s' % kwargs['id']
        queryset = models.DentalClinic.objects.raw(retrieve_query)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        old_data = serializers.DentalClinicSerializer(queryset[0]).data

        updated_data = {k: request.data[k] for k in request.data if
                        old_data.get(k, not request.data[k]) != request.data[k]}
        upd_str = ', '.join(
            f"{key} = '{val}'" if isinstance(val, str) else f"{key} = {val}" for key, val in updated_data.items()
        )

        update_query = f'UPDATE clinics SET %s WHERE id=%s RETURNING *;' % (upd_str, kwargs['id'])
        queryset = models.DentalClinic.objects.raw(update_query)
        serialized_data = serializers.DentalClinicSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        delete_query = 'DELETE FROM clinics WHERE id=%s' % kwargs['id']
        with connection.cursor() as cursor:
            cursor.execute(delete_query)

        return Response({"message": f"Clinic with id {kwargs['id']} has been deleted"}, status=status.HTTP_200_OK)


class ClinicIndexView(APIView):

    def get(self, request):
        query = 'SELECT * FROM clinics'
        clinics = models.DentalClinic.objects.raw(query)
        serialized_clinics = serializers.DentalClinicSerializer(clinics, many=True)
        return Response(serialized_clinics.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not bool(request.data):
            return Response({"message": f"Empty body provided"}, status=status.HTTP_400_BAD_REQUEST)

        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())
        query = f"INSERT INTO clinics (%s) VALUES (%s) RETURNING *;" % (columns, values)
        queryset = models.DentalClinic.objects.raw(query)
        serialized_data = serializers.DentalClinicSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class DentistClinicContractShowView(APIView):

    def get(self, request, **kwargs):
        query = """SELECT dcc.id, 
                   json_build_object(
                                   'id', dcc.id,
                                   'name', dcc.name,
                                   'date', dcc.date,
                                   'clinic', json_build_object(
                                   'id', c.id,
                                   'name', c.name,
                                   'location', c.location,
                                   'description', c.description,
                                   'staff', c.staff,
                                   'opens', c.opens,
                                   'closes', c.closes
                                   ),
                                   'dentist', json_build_object(
                                   'id', d.id,
                                   'name', d.name,
                                   'location', d.location,
                                   'age', d.age,
                                   'specialty', d.specialty
                                   )
                                )
                              FROM clinics c
                              JOIN dentist_clinic_contracts dcc on dcc.clinic_id = c.id
                              JOIN dentists d on d.id = dcc.dentist_id
                              WHERE dcc.id =%s""" % kwargs['id']

        queryset = models.DentistClinicContract.objects.raw(query)
        if len(queryset) == 0:
            return Response({"message": f"Found no DentistClinicContract for this id"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(queryset[0].__dict__['json_build_object'], status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):

        retrieve_query = 'SELECT * FROM dentist_clinic_contracts WHERE id=%s' % kwargs['id']
        queryset = models.DentistClinicContract.objects.raw(retrieve_query)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        old_data = serializers.DentistClinicContractSerializer(queryset[0]).data

        updated_data = {k: request.data[k] for k in request.data if
                        old_data.get(k, not request.data[k]) != request.data[k]}
        upd_str = ', '.join(
            f"{key} = '{val}'" if isinstance(val, str) else f"{key} = {val}" for key, val in updated_data.items()
        )
        update_query = f'UPDATE dentist_clinic_contracts SET %s WHERE id=%s RETURNING *;' % (upd_str, kwargs['id'])
        queryset = models.DentistClinicContract.objects.raw(update_query)
        serialized_data = serializers.DentistClinicContractSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        delete_query = 'DELETE FROM dentist_clinic_contracts WHERE id=%s' % kwargs['id']
        with connection.cursor() as cursor:
            cursor.execute(delete_query)

        return Response({"message": f"DentistClinicContract with id {kwargs['id']} has been deleted"},
                        status=status.HTTP_200_OK)


class DentistClinicContractIndexView(APIView):

    def get(self, request):
        query = """SELECT dcc.id, 
                   json_build_object(
                                   'id', dcc.id,
                                   'name', dcc.name,
                                   'date', dcc.date,
                                   'clinic', json_build_object(
                                   'id', c.id,
                                   'name', c.name,
                                   'location', c.location,
                                   'description', c.description,
                                   'staff', c.staff,
                                   'opens', c.opens,
                                   'closes', c.closes
                                   ),
                                   'dentist', json_build_object(
                                   'id', d.id,
                                   'name', d.name,
                                   'location', d.location,
                                   'age', d.age,
                                   'specialty', d.specialty
                                   )
                                )
                              FROM clinics c
                              JOIN dentist_clinic_contracts dcc on dcc.clinic_id = c.id
                              JOIN dentists d on d.id = dcc.dentist_id
                              """

        queryset = models.DentistClinicContract.objects.raw(query)
        json_list = []
        for obj in queryset:
            json_list.append(obj.__dict__['json_build_object'])
        return Response(json_list, status=status.HTTP_200_OK)

    def post(self, request):

        if not bool(request.data):
            return Response({"message": f"Empty body provided"}, status=status.HTTP_400_BAD_REQUEST)

        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())

        insert_query = 'INSERT INTO dentist_clinic_contracts (%s) VALUES (%s);' % (columns, values)

        # bug in models.DentistClinicContract.objects.raw(insert_query), use cursor
        with connection.cursor() as cursor:
            cursor.execute(insert_query)

        return Response({"message": f"DentistClinicContract has been successfully added without exceptions"},
                        status=status.HTTP_201_CREATED)
