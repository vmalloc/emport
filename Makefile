default: test

test: env
	.venv/bin/pytest

env:
	uv venv
	uv pip install -e ".[testing]"
