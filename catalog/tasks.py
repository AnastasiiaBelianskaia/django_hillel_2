from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email_celery(email, text):
    return send_mail(
        'Notification',
        f'{text}',
        'from@example.com',
        [f'{email}'],
        fail_silently=False,
    )
