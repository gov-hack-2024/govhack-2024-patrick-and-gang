install:
	poetry install

test:
	poetry run pytest tests/

run-streamlit:
	poetry run streamlit run src/app.py

run-fastapi:
	poetry run uvicorn src.main:app --reload

docker-build:
	docker build -t gov-hackathon-project .

docker-run:
	docker run -p 8000:8000 -p 8501:8501 gov-hackathon-project
