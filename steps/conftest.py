import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import Logger
from utils.api_client import APIClient  # Import API client

def pytest_addoption(parser):
    """ Adds command-line arguments for browser and API authentication """
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox"], help="Select browser")
    parser.addoption("--headless", action="store_true", help="Run in headless mode")
    parser.addoption("--client_id", action="store", default="default_client_id", help="API Client ID")
    parser.addoption("--client_secret", action="store", default="default_client_secret", help="API Client Secret")

@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """ Initializes the logger before tests """
    global log_instance
    log_instance = Logger(log_file="../logs/debug_log.log", level="INFO").get_logger()

@pytest.fixture(scope="session")
def driver(request):
    """ Selenium WebDriver fixture """
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def api_client(request):
    """ Initializes APIClient with credentials from CLI or defaults """
    base_url = "https://sandbox-partners-api.airalo.com"
    client_id = request.config.getoption("--client_id")
    client_secret = request.config.getoption("--client_secret")

    if client_id == "default_client_id" or client_secret == "default_client_secret":
        print("⚠️ Using default API credentials. Provide real credentials for valid testing.")

    client = APIClient(base_url, client_id, client_secret)
    client.authenticate()
    return client

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Captures a screenshot on test failure """
    outcome = yield
    report = outcome.get_result()
    if report.failed and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        driver.save_screenshot(f"screenshots/{item.name}.png")
