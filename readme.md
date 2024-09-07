# Government Hackathon Template

This is a template for Gov Hack 2024

## Project Structure

The project directory is organized as follows:

- **`.github/`**: Contains GitHub Actions workflows for Continuous Integration.
  - `workflows/ci.yml`: CI configuration file.

- **`data/`**: Stores data files.
  - `raw/`: Contains raw government data files.
    - `gov_data.csv`: Example of raw data.
  - `processed/`: Contains processed data files.
    - `cleaned_data.csv`: Example of processed data.

- **`docs/`**: Documentation related to the project.
  - `API_Documentation.md`: Documentation for API endpoints or other technical details.

- **`notebooks/`**: Jupyter notebooks for data exploration and analysis.
  - `data_analysis.ipynb`: Example notebook for analyzing data.

- **`src/`**: Source code for the project.
  - `__init__.py`: Initializes the `src` directory as a package.
  - `app.py`: Streamlit application script for the frontend.
  - `data_loader.py`: Module for loading and preprocessing data.
  - `main.py`: FastAPI application script for the backend.
  - `models/`: Contains machine learning model code.
    - `ml_model.py`: Defines and handles the machine learning model.
  - `services/`: Contains code for interacting with external APIs.
    - `api_service.py`: Example service for external API interactions.
  - `utils/`: Utility functions used across the project.
    - `helpers.py`: Example utility functions.
  - `routers/`: FastAPI route handlers.
    - `prediction.py`: API route for making predictions.

- **`tests/`**: Unit and integration tests.
  - `test_app.py`: Tests for the Streamlit app.
  - `test_ml_model.py`: Tests for the machine learning model.
  - `test_api.py`: Tests for FastAPI endpoints.

- **`.env.example`**: Example environment variable file. Copy and rename to `.env` and set your configuration.

- **`.gitignore`**: Specifies files and directories to ignore in Git.

- **`LICENSE`**: License file for the project (MIT License).

- **`README.md`**: This file. Provides an overview, setup instructions, and usage examples.

- **`pyproject.toml`**: Poetry configuration file for managing dependencies and project setup.

- **`poetry.lock`**: Poetry lock file for deterministic dependency management.

- **`Dockerfile`**: Dockerfile for containerizing the application.

- **`Makefile`**: Makefile to automate common tasks like `make test` or `make run`.

## Setup Instructions

### Prerequisites

- **Python 3.10**: Ensure Python 3.10 is installed on your system.
- **Poetry**: Used for managing project dependencies.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/gov-hack-2024/govhack-template.git
   cd gov-hackathon-project

### Installation

2. **Install Dependencies**

   Install [Poetry](https://python-poetry.org/docs/#installation) if you haven’t already. Then, run:

   ```bash
   poetry install

### Set Up Environment Variables

Copy the example environment file and set up your environment variables:

## Running the Project

1. **Start FastAPI Backend**
Run the FastAPI server with:
```bash
run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

This command starts the FastAPI backend on port 8000.

2.**Start Streamlit Frontend**
In a new terminal window, start the Streamlit app with:
```bash
streamlit run src/app.py
```
The Streamlit app will be accessible at http://localhost:8501.