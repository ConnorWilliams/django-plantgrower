HOST=127.0.0.1
TEST_PATH=./
.PHONY: clean-pyc clean-build

clean:
	make clean-pyc
	make clean-build

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	# name '*~' -exec rm -f  {}

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

lint:
	flake8

test: clean-pyc
  py.test --verbose --color=yes $(TEST_PATH)

run:
	python manage.py runserver
