from django.core.mail import send_mail


def send_email(address,subject, body, from_user):
    send_mail(
        subject=subject,
        message=body,
        from_email=from_user,
        recipient_list=[address],
    )