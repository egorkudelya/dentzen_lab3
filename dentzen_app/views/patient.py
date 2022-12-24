from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Patient, Appointment
from ..orm import PGRepository

class PatientShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.patient_repository = PGRepository(Patient)

  def get(self, request, **kwargs):
    obj = self.patient_repository.get(kwargs['id'])
    return (
        Response(obj, status=status.HTTP_200_OK)
        if obj is not None
        else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def patch(self, request, **kwargs):
    obj = self.patient_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    return (
      Response(
        { "message": f"Patient with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.patient_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

class PatientIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.patient_repository = PGRepository(Patient)

  def get(self, request):
    return Response(self.patient_repository.find(), status=status.HTTP_200_OK)

  def post(self, request):
    return Response(
      self.patient_repository.create(request.data),
      status=status.HTTP_201_CREATED,
    )

class PatientAppointmentView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.appointment_repository = PGRepository(Appointment)

  def get(self, request, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute(f'''select json_agg(appointments) from ({
        self.appointment_repository
          .query('a')
          .where(f'a.patient_id = {kwargs["patient_id"]}')
          .join('dentists as d', 'a.dentist_id = d.id', join_type='INNER')
          .select(
            'a.id as appointment_id',
            'a.name as appointment_name',
            'a.date_time as appointment_date_time',
            'a.location as appointment_location',
            'd as dentist',
          )
          .sql()
      }) as appointments''')

      return Response(
        cursor.fetchone()[0],
        status=status.HTTP_200_OK
      )
