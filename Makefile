HOST=127.0.0.1
TEST_PATH=./
.PHONY: clean-pyc clean-build

clean:
	make clean-pyc
	make flush

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	# name '*~' -exec rm -f  {}

flush:
	python manage.py flush --noinput

lint:
	flake8 .

test: clean-pyc
	pytest --cov-report term-missing --cov-config .coveragerc --cov=plantgrower -vv

run-dev:
	beatserver plant_grower.asgi:channel_layer &
	python manage.py runserver &

kill-dev:
	for pid in `ps -l | grep python | awk ' {print $$2} '` ; do kill $$pid ; done
	for pid in `ps -l | grep redis-server | awk ' {print $$2} '` ; do kill $$pid ; done

run:
	python manage.py runworker &
	python manage.py update_grow &
	daphne -b 0.0.0.0 -p 8001 plant_grower.asgi:channel_layer &

kill:
	for pid in `ps -l | grep python | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep daphne | awk ' {print $$4} '` ; do kill $$pid ; done
