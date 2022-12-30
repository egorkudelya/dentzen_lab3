from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Dentist, Appointment, Patient
from ..orm import PGRepository

class DentistShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dentist_repository = PGRepository(Dentist)

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
    return (
      Response(
        { "message": f"Dentist with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.dentist_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )


class DentistIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dentist_repository = PGRepository(Dentist)

  def get(self, request):
    return Response(self.dentist_repository.find(), status=status.HTTP_200_OK)

  def post(self, request):
    return Response(
      self.dentist_repository.create(request.data),
      status=status.HTTP_201_CREATED,
    )

class DentistAppointmentView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.appointment_repository = PGRepository(Appointment)

  def get(self, request, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute(f'''select COALESCE(json_agg(appointments), '[]'::json) from ({
        self.appointment_repository
          .query('a')
          .where(f'a.dentist_id = {kwargs["dentist_id"]}')
          .join(f'{Patient._meta.__dict__["db_table"]} as p', 'a.patient_id = p.id', join_type='INNER')
          .select(
            'a.id as appointment_id',
            'a.name as appointment_name',
            'a.date_time as appointment_date_time',
            'a.location as appointment_location',
            'p as patient',
          )
          .sql()
      }) as appointments''')

      return Response(
        cursor.fetchone()[0],
        status=status.HTTP_200_OK
      )
