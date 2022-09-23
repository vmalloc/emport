default: test

test: env
	.env/bin/pytest

env: .env/.up-to-date

.env/.up-to-date: Makefile pyproject.toml
	python -m venv .env
	.env/bin/pip install -U setuptools pip
	.env/bin/pip install -e '.[testing]'
	touch .env/.up-to-date

