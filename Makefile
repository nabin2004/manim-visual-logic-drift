.PHONY: setup install clean test render evaluate train-rft gen-data dashboard report lint

# Project variables
PYTHON = python3
PIP = pip
MVLD = mvld

setup:
	$(PIP) install -e .

install:
	$(PIP) install -r requirements.txt

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache
	rm -rf media/ results/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

test:
	pytest tests/

# Research Automation Commands
render:
	$(PYTHON) -m mvld.cli.main render file samples/basic_scene.py

evaluate:
	$(PYTHON) -m mvld.cli.main evaluate visual media/images/Scene/Scene_0.png "A blue square and a red circle"

train-rft:
	$(PYTHON) -m mvld.cli.main train algorithm rft --num-samples 10 --rft-threshold 0.7

gen-data:
	$(PYTHON) -m mvld.cli.main data generate-bulk --num 50 --output data/synthetic_bulk.jsonl

dashboard:
	streamlit run mvld/cli/dashboard.py

report:
	$(PYTHON) -m mvld.cli.report

lint:
	black .
	isort .
	flake8 .

# Help command
help:
	@echo "MVLD Makefile - Research Automation"
	@echo "-----------------------------------"
	@echo "setup        : Install package in editable mode"
	@echo "install      : Install dependencies"
	@echo "clean        : Remove build artifacts and temporary media"
	@echo "test         : Run unit tests"
	@echo "render       : Render samples/basic_scene.py"
	@echo "evaluate     : Evaluate the latest render"
	@echo "train-rft    : Run the RFT training algorithm"
	@echo "gen-data     : Generate 50 synthetic samples"
	@echo "dashboard    : Launch the visual results dashboard"
	@echo "report       : Generate summary research reports"
	@echo "lint         : Format and lint code"
