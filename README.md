# Setup

## Prerequisites

Before you start, ensure you have the following prerequisites installed on your machine:

- Python 3.x
- [Git](https://git-scm.com/)

## Installation

1. **Clone the repository to your local machine:**

    ```bash
    git clone https://github.com/giauphan/recapcha-google-audio.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd recapcha-google-audio
    ```

3. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. **Install the project dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` file in the project root and set the required environment variables. Example:**

    ```plaintext
    url_bcdn=https://example.com
    url_find_bcdn=https://example.com
    ```

    Update the URLs based on your specific requirements.

## Running the Script

1. **Run the script:**

    ```bash
    python3 capcha.py
    ```

    Replace `capcha.py` with the name of the script you want to execute.

2. **Follow the on-screen instructions and observe the output.**

## Deactivation (If you used a virtual environment)

When you're done, deactivate the virtual environment:

```bash
deactivate
