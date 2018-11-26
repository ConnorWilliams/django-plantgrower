FROM python:3.5.6

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /var/log/plantgrower
RUN touch /var/log/plantgrower/plantgrower.log
COPY . .
# RUN celery -A plant_grower beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
# RUN celery -A plant_grower worker
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
