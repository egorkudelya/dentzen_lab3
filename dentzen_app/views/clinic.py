from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import DentalClinic
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
