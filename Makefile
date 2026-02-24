.PHONY: setup install clean test run-demo

setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -e .

install:
	pip install -e .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist
	rm -rf media

test:
	pytest tests/

render-test:
	python -m mvld.sandbox.executor --script samples/simple_scene.py
