default: test

test: env
	.env/bin/py.test

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile test_requirements.txt
	python -m virtualenv .env
	.env/bin/pip install -e .
	.env/bin/pip install -r test_requirements.txt
	touch .env/.up-to-date

