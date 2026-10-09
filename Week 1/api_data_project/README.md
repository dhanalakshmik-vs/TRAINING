# REST API Data Processing Project

## Project Overview

This project fetches user data from a REST API, validates the response, transforms the required fields, and exports the processed data into JSON and CSV files.

It also includes exception handling, logging, and unit tests to improve reliability and maintainability.

## Features

* Fetch user data from a REST API using Python `requests`.
* Handle HTTP errors, network errors, request timeouts, and invalid JSON responses.
* Validate API response data and required fields.
* Transform user records by extracting the ID, name, email, and city.
* Export transformed data to JSON and CSV files.
* Log application activities and errors.
* Test validation and transformation functions using Python's built-in `unittest` framework.

## Technologies Used

* Python
* REST API
* Requests
* JSON
* CSV
* Logging
* Unittest

## Project Structure

```text
api_data_project/
├── main.py
├── validators.py
├── transformer.py
├── file_handler.py
├── logging_config.py
├── test_api.py
├── requirements.txt
├── README.md
├── users.json
├── users.csv
└── app.log
```

**File descriptions:**

* `main.py` — Controls the API data processing workflow.
* `validators.py` — Validates the API response and user records.
* `transformer.py` — Extracts the required fields from user data.
* `file_handler.py` — Saves transformed data to JSON and CSV files.
* `logging_config.py` — Configures application logging.
* `test_api.py` — Contains unit tests for validation and transformation.
* `requirements.txt` — Lists the Python package dependencies.
* `users.json` — Stores transformed user data in JSON format.
* `users.csv` — Stores transformed user data in CSV format.
* `app.log` — Records application activity and errors.

The output files and log file are generated when the application runs successfully and logging is configured.

## API Used

This project uses the JSONPlaceholder Users API:

https://jsonplaceholder.typicode.com/users

The API provides sample user records for testing and learning purposes. No API key is required.

## Requirements

* Python 3.9 or later
* pip
* Internet connection to access the API

## Installation and Setup

### 1. Clone the repository

```bash
git clone <github-repository-url>
cd api_data_project
```

Replace `<github-repository-url>` with actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv apienv
```

### 3. Activate the virtual environment

On Windows:

```bash
apienv\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## How to Run the Application

Run the following command from the project directory:

```bash
python main.py
```

The application will:

1. Send a request to the API.
2. Check the HTTP response and parse the JSON data.
3. Validate the received data.
4. Transform the valid records.
5. Save the transformed records to `users.json` and `users.csv`.
6. Record application events in `app.log`.

### Expected Output

```text
Validation successful. Received 10 users.
Transformation successful. Processed 10 users.
Data saved to users.json successfully.
Data saved to users.csv successfully.
```

The exact output may vary if an API request or file operation fails.

## Output Data

Each transformed user record contains the following fields:

| Field   | Description          |
| ------- | -------------------- |
| `id`    | User ID              |
| `name`  | User's name          |
| `email` | User's email address |
| `city`  | User's city          |

Example JSON record:

```json
{
    "id": 1,
    "name": "Leanne Graham",
    "email": "Sincere@april.biz",
    "city": "Gwenborough"
}
```

The CSV file contains the same fields as columns, with one user per row.

## Logging

The application uses Python's built-in `logging` module.

Logs are written to `app.log` and can include:

* Successful API requests
* Validation results
* Transformation activity
* JSON and CSV export results
* API request and file operation errors

Log messages help with debugging and understanding the application's execution.

## Running Unit Tests

The project uses Python's built-in `unittest` framework.

Run the tests using:

```bash
python -m unittest test_api -v
```

The tests cover valid and invalid API data, missing fields, invalid values, and transformation of one or more user records.

The current test suite contains eight tests, all of which passed during development.

## Error Handling

The application handles expected errors, including:

* Network and HTTP request errors
* Request timeouts
* Invalid JSON responses
* Invalid or missing required data
* File operation errors

Validation helps identify incorrect API data before it is transformed.

## Known Limitations

* The application uses a public sample API rather than a production API.
* The output files are overwritten when the application runs again.
* The project processes user records without a database.
* Unit tests focus on validation and transformation; API failures and file export behavior are not comprehensively tested.

## Future Improvements

* Add unit tests for API request failures and file operations.
* Expand validation for nested fields such as `address.city`.
* Add automated test coverage reporting.
* Support configurable API URLs and output file paths.

## Author

Developed as a Python REST API data processing project.
