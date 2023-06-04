from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_review_email(email, phone, text):

    context = {
        'email': email,
        'phone': phone,
        'text': text,
    }

    email_subject = 'Ваши данные в письме'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)

def send_message_email(email, content, tag):

    context = {
        'email': email,
        'content': content,
        'tag': tag,
    }

    email_subject = 'Ваши данные в письме'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [email, ],
    )
    return email.send(fail_silently=False)