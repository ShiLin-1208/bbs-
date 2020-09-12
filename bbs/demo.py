from celery import Celery
import time

celery = Celery("task", broker="redis://127.0.0.1:6379/0", backend="redis://127.0.0.1:6379/0")
# celery -A demo.celery worker --logleve=info --pool=solo 监控
# 在windows运行 加上 --pool=solo
@celery.task
def send_mail():
    print("邮件发送")
    time.sleep(2)
    print("发送完毕")