from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Patient
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
