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
