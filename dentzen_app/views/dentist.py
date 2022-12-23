from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Dentist
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
