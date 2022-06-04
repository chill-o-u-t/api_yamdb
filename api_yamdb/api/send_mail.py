from django.core.mail import EmailMessage


def send_mail(email, confirmation_code):
    mail_subject = 'Activate your account.'
    message = f'{confirmation_code}'
    print('--confirmation_code--')
    print(message)
    email = EmailMessage(
        mail_subject, confirmation_code, to=[email]
    )
    email.send()
