import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..odm.mongo_odm import MongoODM


class ClinicCommentsIndexView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.odm = MongoODM()

    def get(self, request, parent_id):
        obj = self.odm.find_many('clinic_comments', 'clinic_id', parent_id)

        if obj:
            return Response(obj, status=status.HTTP_200_OK)
        return Response(obj, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, parent_id):
        if request.data is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.data['clinic_id'] = parent_id
        request.data['date'] = datetime.datetime.utcnow()

        document = self.odm.insert(collection_name='clinic_comments', data=request.data)

        if not document:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({'inserted_id': str(document.inserted_id)}, status=status.HTTP_201_CREATED)


class ClinicCommentsShowView(APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.odm = MongoODM()

    def get(self, request, **kwargs):
        obj = self.odm.find_one(
            'clinic_comments',
            parent_name='clinic_id',
            parent_id=kwargs['parent_id'],
            comment_id=kwargs['comment_id']
        )
        if obj:
            return Response(obj, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, **kwargs):
        request.data['_id'] = kwargs['comment_id']
        updated_obj = self.odm.update_one(
            'clinic_comments',
            request.data,
            kwargs['comment_id']
        )
        if updated_obj:
            return Response(updated_obj, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        res = self.odm.delete_one(
            'clinic_comments',
            kwargs['comment_id']
        )
        if res:
            return Response(res, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
