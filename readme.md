# Government Hackathon 2024 Project

Patrick and Gang leverage the Australian writing style by empowering GenAI.

## Meet the team
  - Pichaphop Sunthornjittanon (Patrick)
  - Supanuth Amorntiyanggoon (Scott)
  - Jakrapun Sangchan (Jack)
  - Jirarote Jirasirikul (JJ)

## Project Structure

The project directory is organized as follows:

- **`.github/`**: Contains GitHub Actions workflows for Continuous Integration.
  - `workflows/ci.yml`: CI configuration file.

- **`data/`**: Stores data files.
  - `raw/`: Contains raw government data files.
    - `gov_data.csv`: Example of raw data.
  - `processed/`: Contains processed data files.
    - `cleaned_data.csv`: Example of processed data.

- **`src/`**: Source code for the project.
  - `__init__.py`: Initializes the `src` directory as a package.
  - `app.py`: Streamlit application script for the front end.
  - `content_check.py`: OpenAI application to set up prompt OpenAI parameter and return the response.
  - `content_creator.py`: OpenAI application to set up fassi backend on the fly database and generate the content based on the objective.
  - `text_to_speech.py`: Google text-to-speech application to transform text file to voice .mp3.
  - `translator.py`: OpenAI application to translate English into the designated language.
  - `main.py`: FastAPI application script for the backend.


- **`.env.example`**: Example environment variable file. Copy and rename to `.env` and set your configuration.

- **`.gitignore`**: Specifies files and directories to ignore in Git.

- **`LICENSE`**: License file for the project (MIT License).

- **`README.md`**: This file. Provides an overview, setup instructions, and usage examples.

- **`pyproject.toml`**: Poetry configuration file for managing dependencies and project setup.

- **`poetry.lock`**: Poetry lock file for deterministic dependency management.

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

1.**Start Streamlit Frontend**
In a new terminal window, start the Streamlit app with:
```bash
streamlit run src/app.py
```
The Streamlit app will be accessible at http://localhost:8501.
