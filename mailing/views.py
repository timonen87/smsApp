from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Mailing, Message, Client
from .serializers import MailingSerializer, MessageSerializer, ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def totalstat(self, request, pk=None):
        """
        Статистика по каждому сообщению из рассылки

        :param request:
        :param pk:
        :return:
        """
        mailings = Mailing.objects.all()
        get_object_or_404(mailings, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def fullstat(self, request):
        """
        Общая статистика по всем рассылкам
        :param request:
        :return:
        """
        count = Mailing.objects.count()
        # Берем из базы данных общее количество созданных рассылок
        mailings = Mailing.objects.values('id')
        # Берем из базы данных  id рассылок
        message_stat = {}
        # Создаем словарь, где будует храниться статистика
        fullstat = {
            'total count mailings': count,
            'results': message_stat,
        }



        for mailing in mailings:
            # Создаем словарь для статистики по каждому сообщению
            result = {'total messages': 0, 'sent': 0, 'no sent': 0}

            message_db = Message.objects.filter(mailing_id=mailing['id']).all()
            send_messages = message_db.filter(msg_status='sent').count()
            no_sent_messages = message_db.filter(msg_status='so sent').count()
            result['total messages'] = len(message_db)
            result['sent'] = send_messages
            result['no sent'] = no_sent_messages
            message_stat[mailing['id']] = result

        fullstat['results'] = message_stat
        return Response(fullstat)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


