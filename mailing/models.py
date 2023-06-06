import pytz
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Mailing(models.Model):
    date_start = models.DateTimeField(verbose_name='Дата запуска рассылки')
    date_end = models.DateTimeField(verbose_name='Дата окончания рассылки')
    time_start = models.TimeField(verbose_name='Время начала отправки сообщений')
    time_end = models.TimeField(verbose_name='Время окончаня отправки сообщений')
    content = models.TextField(max_length=300, verbose_name='Текст сообщения')
    tag = models.CharField(max_length=50, verbose_name='Теги', blank=True)
    mobile_code = models.CharField(max_length=3, blank=True, verbose_name='Код оператора мобильной связи')


    @property
    def valide_date(self):
        return bool(self.date_start <= timezone.now() <= self.date_end)

    def __str__(self):
        return f'Рссылка № {self.id} | от: {self.date_start}  | до : {self.date_end}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    num_valide = RegexValidator(
        regex=r"^7\d{10}$",
        message="Номер телефона должен быть введен в формате: '+7XXXXXXXXX'.(X - цифра от 0 до 9) ",
    )

    phone_number = models.CharField(max_length=11, validators=[num_valide], verbose_name='Номер телефона', unique=True )
    mobile_code = models.CharField(max_length=3,  verbose_name='Код оператора мобильной связи', editable=False)
    tag = models.CharField(max_length=100, blank=True, verbose_name="Теги")
    timezone = models.CharField(max_length=32, choices=TIMEZONES, verbose_name='Часовой пояс', default="UTC")

    def save(self, *args, **kwargs):
        self.mobile_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)



    def __str__(self):
        return f'Клиент #{self.id} с номером {self.phone_number}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    SENT = 'sent'
    NO_SENT = 'no sent'

    STATUS_CHOICES = [
        (SENT, 'sent'),
        (NO_SENT, 'no sent'),
    ]

    created_at = models.DateTimeField(verbose_name="дата и время создания (отправки)", auto_now_add=True)
    msg_status = models.CharField(
        verbose_name="статус отправки", max_length=10, choices=STATUS_CHOICES
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name="messages")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="messages")


    def __str__(self):
        return f'Сообщение #{self.id} - {self.mailing} было отпрвлено клиенту {self.client}'

    class Meta:
        verbose_name = 'Сообщеине'
        verbose_name_plural = 'Сообщения'








