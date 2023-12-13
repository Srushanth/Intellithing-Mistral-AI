install:
	pip install -r ./requirements.txt

venv-python:
	python -m venv .venv

venv-conda:
	conda create -p .venv python==3.11 -y

activate-conda:
	conda activate .venv/

upgrade-pip:
	python.exe -m pip install --upgrade pip

