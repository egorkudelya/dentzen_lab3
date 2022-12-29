from django.http import HttpResponseNotFound
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class ITestClient:

    def __init__(self, prefix):
        super().__init__()
        self.client = APIClient()
        self.prefix = prefix

    def testPost(self, data):
        res = self.client.post(path=self.prefix, data=data, format='json')
        assert type(res) != HttpResponseNotFound
        return res

    def testGet(self, id):
        res = self.client.get(self.prefix + str(id) + '/')
        assert type(res) != HttpResponseNotFound
        return res

    def testPatch(self, id, data):
        return self.client.patch(self.prefix + str(id) + '/', data)

    def testDelete(self, id):
        return self.client.delete(self.prefix + str(id) + '/')


class IRunnableTestClient(ITestClient):

    def __init__(self, prefix):
        super().__init__(prefix)
        self.client = ITestClient(self.prefix)

    def runPostTest(self, data):
        response = super().testPost(data)
        entity_id = response.data.pop('id', None)

        assert response.status_code == status.HTTP_201_CREATED
        assert data == response.data
        return entity_id

    def runPatchTest(self, id, data):
        entity = self.runGetTest(id).data

        response = super().testPatch(id, data)
        response.data.pop('id', None)

        entity.update(data)

        assert response.status_code == status.HTTP_200_OK
        assert entity == response.data
        return response

    def runGetTest(self, id):
        response = super().testGet(id)
        response.data.pop('id', None)

        assert response.status_code == status.HTTP_200_OK
        return response

    def runDeleteTest(self, id):
        response = super().testDelete(id)

        assert response.status_code == status.HTTP_200_OK
        return response

    def runCRUDTest(self, post_data, patch_data):
        entity_id = self.runPostTest(post_data)
        patch_response = self.runPatchTest(entity_id, patch_data)
        get_response = self.runGetTest(entity_id)

        assert patch_response.data == get_response.data
        for key, item in patch_data.items():
            assert patch_response.data[key] == item

        delete_response = self.runDeleteTest(entity_id)


class TestClinic(IRunnableTestClient, APITestCase):

    def __init__(self, _):
        super().__init__('/clinics/')

    def runTest(self):
        post_data = \
            {
                "name": "Random Clinic",
                "description": "Random Description",
                "staff": 121,
                "location": "Ohio",
                "opens": "08:00:00",
                "closes": "20:00:00"
            }

        patch_data = \
            {
                "name": "Updated Clinic Name",
                "staff": 108
            }

        self.runCRUDTest(post_data, patch_data)


class TestDentist(IRunnableTestClient, APITestCase):

    def __init__(self, _):
        super().__init__('/dentists/')

    def runTest(self):
        post_data = \
            {
                "name": "Random Dentist",
                "location": "Kyiv",
                "specialty": "Something123",
                "age": 47
            }

        patch_data = \
            {
                "name": "Updated Dentist",
                "location": "New York"
            }

        self.runCRUDTest(post_data, patch_data)


class TestSupplier(IRunnableTestClient, APITestCase):

    def __init__(self, _):
        super().__init__('/suppliers/')

    def runTest(self):
        post_data = \
            {
                "name": "Random Company",
                "description": "A medical supply company",
                "years_on_market": 11,
                "location": "Kyiv"
            }

        patch_data = \
            {
                "name": "Updated Company",
                "location": "New York"
            }

        self.runCRUDTest(post_data, patch_data)


class TestPatient(IRunnableTestClient, APITestCase):

    def __init__(self, _):
        super().__init__('/patients/')

    def runTest(self):
        post_data = \
            {
                "name": "Random Name",
                "age": 99
            }

        patch_data = \
            {
                "age": 48
            }

        self.runCRUDTest(post_data, patch_data)
