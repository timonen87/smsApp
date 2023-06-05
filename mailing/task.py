import os
import datetime
from dotenv import load_dotenv
import pytz
import requests

from celery.utils.log import get_task_logger
from core.celery import app

logger = get_task_logger(__name__)

load_dotenv()
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id, url=URL, token=TOKEN):
    from .models import Mailing, Message, Client
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.datetime.now(timezone)
    api_url = url + str(data["id"])

    if mailing.time_start <= now.time() <= mailing.time_end:
        header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        try:
            requests.post(api_url, headers=header, json=data)
        except requests.exceptions.RequestException as ex:
            logger.info(f'Сообщение {data["id"]} с ошибкой {ex}')
        else:
            logger.info(f'Сообщение {data["id"]} успешно отправлено')
            Message.objects.filter(pk=data['id']).update(msg_status='sent')
    else:
        logger.info(
            f"Сообщение {data['id']} будет отправлено повтороно через {3600} секунд"
        )
        return self.retry(countdown=3600)






