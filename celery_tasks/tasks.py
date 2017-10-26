from  celery import task
from django.core.mail import send_mail
from django.conf import settings
# import djcelery
# djcelery.setup_loader()
# BROKER_URL = 'redis://127.0.0.1:6379/2'
# CELERY_IMPORTS = ('celery_tasks.tasks')

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
#
# import django
# django.setup()
# app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/2')

# @task
# def show():
#
#     print('hello')
#     time.sleep(5)
#     print('world')
@task
def send_email(token, username, email):
    '''发送激活邮件'''
    subject = '天天生鲜用户'  # 标题
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [email]  # 收件人列表
    html_message = '<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token

    send_mail(subject, message, sender, receiver, html_message=html_message)




