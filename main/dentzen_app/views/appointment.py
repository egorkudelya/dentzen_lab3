from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Appointment, Patient
from ..orm import PGRepository

class AppointmentShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.appointment_repository = PGRepository(Appointment)

  def get(self, request, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute(f'''select row_to_json(appointment) from ({
        self.appointment_repository
          .query('a')
          .where(f"a.id = {kwargs['id']}")
          .join('dentists as d', 'd.id = a.dentist_id')
          .join(f'{Patient._meta.__dict__["db_table"]} as p', 'p.id = a.patient_id')
          .select(
            'a.id',
            'a.name',
            'a.location',
            'a.date_time',
            'd as dentist',
            'p as patient',
          )
          .sql()
      }) appointment''')

      return Response(cursor.fetchone()[0], status=status.HTTP_200_OK)

  def patch(self, request, **kwargs):
    obj = self.appointment_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    return (
      Response(
        { "message": f"Appointment with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.appointment_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )


class AppointmentIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.appointment_repository = PGRepository(Appointment)

  def get(self, request):
    with connection.cursor() as cursor:
      cursor.execute(f'''select json_agg(appointments) from ({
        self.appointment_repository
          .query('a')
          .join('dentists as d', 'd.id = a.dentist_id')
          .join(f'{Patient._meta.__dict__["db_table"]} as p', 'p.id = a.patient_id')
          .select(
            'a.id',
            'a.name',
            'a.location',
            'a.date_time',
            'd as dentist',
            'p as patient',
          )
          .sql()
      }) appointments''')

      return Response(cursor.fetchone()[0], status=status.HTTP_200_OK)

  def post(self, request):
    return (
      Response(
        self.appointment_repository.create(request.data),
        status=status.HTTP_201_CREATED,
      )
    )
