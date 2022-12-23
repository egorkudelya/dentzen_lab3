from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import DentistClinicContract
from ..orm import PGRepository

class DentistClinicContractShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.contract_repository = PGRepository(DentistClinicContract)

  def get(self, request, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute(f'''select row_to_json(contract) from ({
        self.contract_repository
          .query('dcc')
          .where(f"dcc.id = {kwargs['id']}")
          .join('dentists as d', 'd.id = dcc.dentist_id')
          .join('clinics as c', 'c.id = dcc.clinic_id')
          .select(
            'dcc.id',
            'dcc.name',
            'dcc.date',
            'd as dentist',
            'c as clinic'
          )
          .sql()
      }) contract''')

      return Response(cursor.fetchone()[0], status=status.HTTP_200_OK)

  def patch(self, request, **kwargs):
    obj = self.contract_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    return (
      Response(
        { "message": f"Contract with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.contract_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )


class DentistClinicContractIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.contract_repository = PGRepository(DentistClinicContract)

  def get(self, request):
    with connection.cursor() as cursor:
      cursor.execute(f'''select json_agg(contracts) from ({
        self.contract_repository
          .query('dcc')
          .join('dentists as d', 'd.id = dcc.dentist_id')
          .join('clinics as c', 'c.id = dcc.clinic_id')
          .select(
            'dcc.id',
            'dcc.name',
            'dcc.date',
            'd as dentist',
            'c as clinic'
          )
          .sql()
      }) contracts''')

      return Response(cursor.fetchone()[0], status=status.HTTP_200_OK)

  def post(self, request):
    return (
      Response(
        self.contract_repository.create(request.data),
        status=status.HTTP_201_CREATED,
      )
    )
