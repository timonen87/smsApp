from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from mailing.models import Mailing, Client


class TestMethod(APITestCase):
    def test_mailing(self):
        new_mailing = {
            "date_start": now(),
            "date_end": now(),
            "time_start": now().time(),
            "time_end": now().time(),
            "content": "text",
            "tag": "megafon",
            "mobile_code": "926",
        }
        response = self.client.post('http://127.0.0.1:8080/api/mailings/', new_mailing)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tag'], 'megafon')
        self.assertEqual(response.data['mobile_code'], "926")
        self.assertIsInstance(response.data['mobile_code'], str)

    def test_clients(self):
        client_count = Client.objects.all().count()
        new_client = {
                "phone_number": "79674653674",
                "tag": "mts",
                "timezone": "UTC",
            }
        response = self.client.post("http://127.0.0.1:8080/api/clients/", new_client)
        self.assertIsInstance(response.data["tag"], str)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), client_count + 1)
        self.assertEqual(response.data["phone_number"], "79674653674")

    def test_mailing_stat(self):
        self.test_mailing()
        url = "http://127.0.0.1:8080/api/mailings"
        response = self.client.get(f"{url}/1/totalstat/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{url}/fullstat/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total count mailings"], 1)
        self.assertIsInstance(response.data["results"], dict)


