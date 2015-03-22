default: test

test: env
	.env/bin/py.test

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile
	python -m virtualenv .env
	.env/bin/pip install -e .
	.env/bin/pip install pytest
	touch .env/.up-to-date

