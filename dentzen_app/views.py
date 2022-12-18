from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .orm.DARepository import DARepository

class DentistShowView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dentist_repository = DARepository(models.Dentist, serializers.DentistSerializer)

    def get(self, request, **kwargs):
        obj = self.dentist_repository.get(kwargs['id'])
        return (
            Response(obj, status=status.HTTP_200_OK)
            if obj is not None
            else Response(status=status.HTTP_404_NOT_FOUND)
        )

    def patch(self, request, **kwargs):
        obj = self.dentist_repository.patch(kwargs['id'], request.data)

        return (
            Response(obj, status=status.HTTP_200_OK)
            if obj is not None
            else Response(status=status.HTTP_404_NOT_FOUND)
        )

    def delete(self, request, **kwargs):
        self.dentist_repository.delete(kwargs['id'])

        return Response({"message": f"Dentist with id {kwargs['id']} has been deleted"}, status=status.HTTP_200_OK)


class DentistIndexView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dentist_repository = DARepository(models.Dentist, serializers.DentistSerializer)

    def get(self, request):
        return Response(self.dentist_repository.find(), status=status.HTTP_200_OK)

    def post(self, request):
        return (
            Response(
                self.dentist_repository.create(request.data),
                status=status.HTTP_201_CREATED,
            )
            if bool(request.data)
            else Response(
                {"message": "Empty body provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        )


class ClinicShowView(APIView):

    def get(self, request, **kwargs):
        query = f"""SELECT DISTINCT c.*, d.*
                   FROM clinics c
                   LEFT JOIN dentist_clinic_contracts dcc on dcc.clinic_id = c.id
                   LEFT JOIN dentists d on d.id = dcc.dentist_id
                   WHERE c.id ={kwargs['id']}"""

        clinics = models.DentalClinic.objects.raw(query)
        serialized_clinics = serializers.DentalClinicSerializer(clinics, many=True)
        return Response(serialized_clinics.data, status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):
        retrieve_query = f"SELECT * FROM clinics WHERE id={kwargs['id']}"
        queryset = models.DentalClinic.objects.raw(retrieve_query)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        old_data = serializers.DentalClinicSerializer(queryset[0]).data

        updated_data = {k: request.data[k] for k in request.data if
                        old_data.get(k, not request.data[k]) != request.data[k]}
        upd_str = ', '.join(
            f"{key} = '{val}'" if isinstance(val, str) else f"{key} = {val}" for key, val in updated_data.items()
        )

        update_query = (
            f"UPDATE clinics SET {upd_str} WHERE id={kwargs['id']} RETURNING *;"
        )
        queryset = models.DentalClinic.objects.raw(update_query)
        serialized_data = serializers.DentalClinicSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        delete_query = f"DELETE FROM clinics WHERE id={kwargs['id']}"
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
            return Response(
                {"message": "Empty body provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())
        query = f"INSERT INTO clinics ({columns}) VALUES ({values}) RETURNING *;"
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
            return Response(
                {"message": "Found no DentistClinicContract for this id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(queryset[0].__dict__['json_build_object'], status=status.HTTP_200_OK)

    def patch(self, request, **kwargs):

        retrieve_query = (
            f"SELECT * FROM dentist_clinic_contracts WHERE id={kwargs['id']}"
        )
        queryset = models.DentistClinicContract.objects.raw(retrieve_query)

        if not queryset:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        old_data = serializers.DentistClinicContractSerializer(queryset[0]).data

        updated_data = {k: request.data[k] for k in request.data if
                        old_data.get(k, not request.data[k]) != request.data[k]}
        upd_str = ', '.join(
            f"{key} = '{val}'" if isinstance(val, str) else f"{key} = {val}" for key, val in updated_data.items()
        )
        update_query = f"UPDATE dentist_clinic_contracts SET {upd_str} WHERE id={kwargs['id']} RETURNING *;"
        queryset = models.DentistClinicContract.objects.raw(update_query)
        serialized_data = serializers.DentistClinicContractSerializer(queryset[0]).data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        delete_query = f"DELETE FROM dentist_clinic_contracts WHERE id={kwargs['id']}"
        with connection.cursor() as cursor:
            cursor.execute(delete_query)

        return Response({"message": f"DentistClinicContract with id {kwargs['id']} has been deleted"},
                        status=status.HTTP_200_OK)


class DentistClinicContractIndexView(APIView):

    def get(self, request):
        query = """
            SELECT
                dcc.id,
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
        json_list = [obj.__dict__['json_build_object'] for obj in queryset]
        return Response(json_list, status=status.HTTP_200_OK)

    def post(self, request):

        if not bool(request.data):
            return Response(
                {"message": "Empty body provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        columns = ', '.join(request.data.keys())
        values = ', '.join(f"'{val}'" for val in request.data.values())

        insert_query = (
            f'INSERT INTO dentist_clinic_contracts ({columns}) VALUES ({values});'
        )

        # bug in models.DentistClinicContract.objects.raw(insert_query), use cursor
        with connection.cursor() as cursor:
            cursor.execute(insert_query)

        return Response(
            {
                "message": "DentistClinicContract has been successfully added without exceptions"
            },
            status=status.HTTP_201_CREATED,
        )
