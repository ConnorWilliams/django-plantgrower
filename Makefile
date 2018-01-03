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

build:
	python ../django-plantgrower/setup.py sdist
	pip install -U ../django-plantgrower/

run-dev:
	beatserver plant_grower.asgi:channel_layer &
	python manage.py runserver &

kill-dev:
	for pid in `ps -l | grep python | awk ' {print $$2} '` ; do kill sigterm $$pid ; done
	for pid in `ps -l | grep beatserver | awk ' {print $$2} '` ; do kill sigterm $$pid ; done
	for pid in `ps -l | grep redis-server | awk ' {print $$2} '` ; do kill sigterm $$pid ; done

run:
	python manage.py runworker &
	beatserver plant_grower.asgi:channel_layer >> /var/log/plantgrower/plantgrower.log &
	daphne -b 0.0.0.0 -p 8001 plant_grower.asgi:channel_layer &

kill:
	for pid in `ps -l | grep python | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep beatserver | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep daphne | awk ' {print $$4} '` ; do kill $$pid ; done
