from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email, ] # 아래와 같은 것
    # if isinstance(to_email, list):
    #     to_email = to_email
    # else:
    #     tod_email = [to_email, ]

    # 제목, 본문, 보내는 사람(현재 개발자 HOST 이기에 settings.EMAIL_HOST_USER 설정함) , 받는 사람
    send_mail(subject, message, settings.EMAIL_HOST_USER ,to_email)