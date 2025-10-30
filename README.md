# My Python Project

## Setup

1. Clone the repo:
    ```bash
    git clone https://github.com/Nooneyouknowof/FSE_TEAM_3_FINAL_PROJECT.git
    ```

2. Open the project
    ```bash
    cd FSE_TEAM_3_FINAL_PROJECT
    ```
    Or
    ```bash
    code FSE_TEAM_3_FINAL_PROJECT
    ```

3. Create a venv for the project
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment
    ```bash
    source venv/bin/activate
    ```

5. Install the python dependencies
    ```bash
    pip install -r requirements.txt
    ```

6. Install linux package "eSpeak-NG"
    ```bash
    sudo apt install espeak-ng
    ```

7. Create the .env file and edit it
    ```bash
    cp .env.example .env
    ```

8. Run the program
    ```bash
    python -m main.py
    ```