from django.utils.timezone import now
from rest_framework.test import APITestCase

from mailing.models import Mailing, Client, Message


class TestModel(APITestCase):
    def test_creates_mailings(self):
        mailing = Mailing.objects.create(
            date_start=now(),
            date_end=now(),
            content="test",
            time_start=now().time(),
            time_end=now().time(),
            tags="mts",
            mobile_code='926'
        )
        self.assertIsInstance(mailing, Mailing)
        self.assertEqual(mailing.tags, "mts")
        self.assertEqual(mailing.mobile_code, "926")

    def test_creates_clients(self):
        client = Client.objects.create(
            phone_number="79268456345",
            m_code="926",
            tag="mts",
            timezone="UTC",
        )
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone_number, '79268456345')

    def test_create_message(self):
        self.test_creates_mailings()
        self.test_creates_clients()
        message = Message.objects.create(
            msg_status='no sent', mailing_id=1, client_id=1,
        )
        self.assertIsInstance(message, Message)
        self.assertEqual(message.msg_status, 'no sent')


