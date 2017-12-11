HOST=127.0.0.1
TEST_PATH=./
.PHONY: clean-pyc clean-build

clean:
	make clean-pyc
	make clean-build
	make flush

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	# name '*~' -exec rm -f  {}

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

flush:
	python manage.py flush --noinput

lint:
	flake8 . --exclude migrations/*,plantgrower/migrations/*

test: clean-pyc
	pytest --cov-report term-missing --cov-config .coveragerc --cov=plantgrower -vv

run-dev:
	python manage.py runworker &
	python manage.py update_grow &
	python manage.py runserver

kill-dev:
	for pid in `ps -l | grep python | awk ' {print $$2} '` ; do kill $$pid ; done
	for pid in `ps -l | grep redid-server | awk ' {print $$2} '` ; do kill $$pid ; done

run:
	python manage.py runworker &
	python manage.py update_grow &
	daphne -b 0.0.0.0 -p 8001 plant_grower.asgi:channel_layer &

kill:
	for pid in `ps -l | grep python | awk ' {print $$4} '` ; do kill $$pid ; done
	for pid in `ps -l | grep daphne | awk ' {print $$4} '` ; do kill $$pid ; done
