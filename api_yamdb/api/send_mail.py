from django.core.mail import EmailMessage


def send_mail(email, confirmation_code):
    mail_subject = 'Activate your account.'
    EmailMessage(
        mail_subject, confirmation_code, to=[email]
    ).send()
