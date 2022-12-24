from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import DentalClinic, DentistClinicContract
from ..orm import PGRepository

class ClinicShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.clinic_repository = PGRepository(DentalClinic)

  def get(self, request, **kwargs):
    obj = self.clinic_repository.get(kwargs['id'])
    return (
        Response(obj, status=status.HTTP_200_OK)
        if obj is not None
        else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def patch(self, request, **kwargs):
    obj = self.clinic_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    return (
      Response(
        { "message": f"Clinic with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.clinic_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

class ClinicIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.clinic_repository = PGRepository(DentalClinic)

  def get(self, request):
    return Response(self.clinic_repository.find(), status=status.HTTP_200_OK)

  def post(self, request):
    return (
      Response(
        self.clinic_repository.create(request.data),
        status=status.HTTP_201_CREATED,
      )
      if bool(request.data)
      else Response(
        {"message": "Empty body provided"},
        status=status.HTTP_400_BAD_REQUEST,
      )
    )

class ClinicDentistsView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.contract_repository = PGRepository(DentistClinicContract)

  def get(self, request, **kwargs):
    print('Hello')
    with connection.cursor() as cursor:
      cursor.execute(f'''select json_agg(contracts) from ({
        self.contract_repository
          .query('dcc')
          .where(f'dcc.clinic_id = {kwargs["clinic_id"]}')
          .join('dentists as d', 'dcc.dentist_id = d.id', join_type='INNER')
          .select(
            'dcc.id as contract_id',
            'dcc.name as contract_name',
            'dcc.date as contract_date',
            'd as dentist',
          )
          .sql()
      }) as contracts''')

      return Response(
        cursor.fetchone()[0], 
        status=status.HTTP_200_OK
      )