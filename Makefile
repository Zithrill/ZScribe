.PHONY: test install clean secure

test:
	pytest tests/

install:
	pip install -r requirements.txt

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

lint:
	flake8 src/ tests/

format:
	black src/ tests/

secure:
	bandit -c bandit.yaml -r .
