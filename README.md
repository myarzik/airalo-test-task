# Airalo Test Automation

## Overview
This project automates UI and API testing for Airalo using Selenium, Pytest, Allure, and Docker.  
It includes:
- UI Tests (Selenium + Pytest + BDD)
- API Tests (Requests + Pytest + Allure)
- Dockerized setup for easy execution

## Prerequisites
Before running the tests, ensure you have the following installed:

- Python 3.9+
- pip (Python package manager)
- Google Chrome (for UI tests)
- ChromeDriver (must match Chrome version)
- Docker (optional, for containerized execution)
- Allure (for test reporting)

### Install Required Python Packages
```sh
pip install -r requirements.txt
```

### UI Tests (Selenium + Pytest + BDD)
```sh
pytest steps/test_search.py –browser chrome –headless –alluredir=allure-results
```
-	–browser chrome runs tests in Google Chrome (use firefox for Firefox).
-   –headless runs the browser in headless mode.
-   –alluredir=allure-results saves test results for Allure reporting.

### API Tests (Requests + Pytest + Allure)
```sh
pytest steps/test_api.py –client_id=“your_client_id” –client_secret=“your_client_secret” –alluredir=allure-results
```
-   –client_id and –client_secret are required for API authentication.

### Running Tests in Docker

#### Build the Docker Image
```sh
docker build -t airalo-tests .
```
#### Run Tests in a Container
```sh
docker run –rm -e CLIENT_ID=“your_client_id” -e CLIENT_SECRET=“your_client_secret” airalo-tests
```
#### Run Tests Using Docker Compose
```sh
docker-compose up –build
```
#### Viewing Test Reports (Allure)

After running the tests, generate and open the Allure report:
```sh
allure serve allure-results
```