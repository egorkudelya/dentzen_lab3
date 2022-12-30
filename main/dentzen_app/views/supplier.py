from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Supplier, Drug, Instrument
from ..orm import PGRepository

class SupplierShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.supplier_repository = PGRepository(Supplier)

  def get(self, request, **kwargs):
    obj = self.supplier_repository.get(kwargs['id'])
    return (
        Response(obj, status=status.HTTP_200_OK)
        if obj is not None
        else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def patch(self, request, **kwargs):
    obj = self.supplier_repository.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    return (
      Response(
        { "message": f"Supplier with id {kwargs['id']} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.supplier_repository.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )


class SupplierIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.supplier_repository = PGRepository(Supplier)

  def get(self, request):
    return Response(self.supplier_repository.find(), status=status.HTTP_200_OK)

  def post(self, request):
    return Response(
      self.supplier_repository.create(request.data),
      status=status.HTTP_201_CREATED,
    )

class SupplierProductsIndexView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.drug_repository = PGRepository(Drug)
    self.instrument_repository = PGRepository(Instrument)

    self.repos = {
      'drug': self.drug_repository,
      'instrument': self.instrument_repository,
    }

  def get(self, request, **kwargs):
    types = [type for type in kwargs.get('type', '').split(',') if type]
    products = []

    for type, repo in ((type, self.repos[type]) for type in types) if len(types) else self.repos.items():
      products.extend(
        { **product, 'type': type} 
        for product in (
          repo
            .query('p')
            .where(f'p.supplier_id = {kwargs["supplier_id"]}')
            .select(f"COALESCE(json_agg(p), '[]'::json)")
            .execute(one=True)[0]
        ) 
      )

    return Response(products, status=status.HTTP_200_OK)

  def post(self, request, **kwargs):
    product_type = kwargs.get('type', None) or request.data.get('type', None)
    repo = self.repos.get(product_type, None)

    if repo is None:
      return Response(
        { "message": "No valid supplier product type was provided" },
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    return Response(
      repo.create({ 
        **request.data, 
        'supplier': kwargs['supplier_id']
      }), 
      status=status.HTTP_201_CREATED,
    )

class SupplierProductShowView(APIView):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.drug_repository = PGRepository(Drug)
    self.instrument_repository = PGRepository(Instrument)

    self.repos = {
      'drug': self.drug_repository,
      'instrument': self.instrument_repository,
    }

  def get(self, request, **kwargs):
    type = kwargs.get('type', None)
    repo = self.repos.get(type, None)

    if repo is None:
      return Response(
        { "message": "No valid supplier product type was provided" },
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    obj = self.repo.get(kwargs['id'])
    return (
        Response(obj, status=status.HTTP_200_OK)
        if obj is not None
        else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def patch(self, request, **kwargs):
    product_type = kwargs.get('type', None) or request.data.get('type', None)
    repo = self.repos.get(product_type, None)

    if repo is None:
      return Response(
        { "message": "No valid supplier product type was provided" },
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    obj = self.repo.patch(kwargs['id'], request.data)

    return (
      Response(obj, status=status.HTTP_200_OK)
      if obj is not None
      else Response(status=status.HTTP_404_NOT_FOUND)
    )

  def delete(self, request, **kwargs):
    type = kwargs.get('type', None)
    repo = self.repos.get(type, None)

    if repo is None:
      return Response(
        { "message": "No valid supplier product type was provided" },
        status=status.HTTP_400_BAD_REQUEST,
      )

    return (
      Response(
        { "message": f"Supplier product with id {kwargs['id']} and type {type} has been deleted" },
        status=status.HTTP_200_OK
      )
      if self.repo.delete(kwargs["id"])
      else Response(status=status.HTTP_404_NOT_FOUND)
    )