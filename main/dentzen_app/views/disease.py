from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Disease, Diagnosis
from ..orm import PGRepository

class DiseaseShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.disease_repository = PGRepository(Disease)
    self.diagnosis_repository = PGRepository(Diagnosis)

  def patch(self, request, **kwargs):
    obj = self.disease_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    diagnosis_id, = (
      self.diagnosis_repository
        .query('da')
        .where(f'da.patient_id = {kwargs["patient_id"]}')
        .and_where(f'da.disease_id = {kwargs["id"]}')
        .select('da.id')
        .execute(one=True)
    )

    if (diagnosis_id and
      self.diagnosis_repository.delete(diagnosis_id) and
      self.disease_repository.delete(kwargs['id'])):
      return Response(
        { "message": f"Diagnosis with id {kwargs['id']} has been deleted from patient with id {kwargs['patient_id']}" },
        status=status.HTTP_200_OK
      )

    return Response(status=status.HTTP_404_NOT_FOUND)

class DiseaseIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.disease_repository = PGRepository(Disease)
    self.diagnosis_repository = PGRepository(Diagnosis)

  def get(self, request, **kwargs):
    return Response(
      self.disease_repository
        .query('ds')
        .join(
          f'{self.diagnosis_repository.table_name} as da',
          f'ds.id = da.disease_id and da.patient_id = {kwargs["patient_id"]}',
          join_type='INNER',
        )
        .select("COALESCE(json_agg(ds.*), '[]'::json)")
        .execute(one=True)[0],
      status=status.HTTP_200_OK,
    )

  def post(self, request, **kwargs):
    disease = self.disease_repository.create(request.data)

    self.diagnosis_repository.create({
      'patient': kwargs['patient_id'],
      'disease': disease['id'],
    })

    return Response(disease, status=status.HTTP_201_CREATED)
