.DEFAULT_GOAL := help

.PHONY: help  # shows available commands
help:
	@echo "\nAvailable commands:\n\n $(shell sed -n 's/^.PHONY:\(.*\)/ *\1\\n/p' Makefile)"


.PHONY: test  # runs tests
test:
	coverage run setup.py test


.PHONY: test_all  # runs tests using detox, combines coverage and reports
test_all:
	tox
	make coverage


.PHONY: coverage  # combines coverage and reports
coverage:
	coverage combine || true
	coverage report


.PHONY: lint
lint:
	flake8


.PHONY: clean  # removes build files
clean:
	rm -rf dist/ build/ .tox/ *.egg-info


.PHONY: build  # builds wheel and tar
build:
	pip install -U twine wheel
	python setup.py sdist bdist_wheel


.PHONY: release  # runs clean, build, and then pushes to pypi
release: clean build
	@echo && echo && echo _____________________ \
	&& echo Check version: new $(shell grep "version =" setup.py) vs old $(shell curl -s https://pypi.python.org/pypi/uwsgi-tools/json | grep '"version"' | xargs)
	@read -p "Release? [yN]: " -n 1 -r; \
	if [ "$$REPLY" == "y" ]; then echo && twine upload -s dist/*; else echo "Aborted."; fi
