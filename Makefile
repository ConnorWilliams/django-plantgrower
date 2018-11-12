HOST=127.0.0.1
TEST_PATH=./
.PHONY: clean-pyc clean-build

clean:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.sqlite3' -delete
	find . -name 'dump.rdb' -delete
	# name '*~' -exec rm -f  {}

flush:
	python manage.py flush --noinput

lint:
	flake8 .

rebuild: kill-dev
	pipenv install ../django-plantgrower/
	make run-dev

run-dev:
	redis-server &
	python manage.py runserver &
	celery -A plant_grower beat --scheduler django_celery_beat.schedulers:DatabaseScheduler &
	celery -A plant_grower worker &

kill-dev:
	for pid in `ps auxw | grep 'manage.py runserver' | grep -v grep | awk ' {print $$2} '` ; do echo $$pid; kill $$pid ; done
	for pid in `ps auxw | grep 'django_celery_beat' | grep -v grep | awk ' {print $$2} '` ; do echo $$pid; kill $$pid ; done
	for pid in `ps auxw | grep celery | grep -v grep | awk ' {print $$2} '` ; do echo $$pid; kill $$pid ; done
	for pid in `ps auxw | grep redis | grep -v grep | awk ' {print $$2} '` ; do echo $$pid; kill $$pid ; done

run:
	python manage.py runworker &
	beatserver plant_grower.asgi:channel_layer >> /var/log/plantgrower/plantgrower.log &
	daphne -b 0.0.0.0 -p 8001 plant_grower.asgi:channel_layer &

kill:
	for pid in `ps -l | grep python | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep beatserver | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep daphne | awk ' {print $$4} '` ; do kill $$pid ; done
