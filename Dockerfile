FROM arm32v7/python:3.7-alpine

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r requirements.txt
RUN mkdir /var/log/plantgrower
RUN touch /var/log/plantgrower/plantgrower.log
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
