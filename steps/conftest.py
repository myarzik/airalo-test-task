import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import Logger  # Импортируем стандартный логгер


def pytest_addoption(parser):
    """ Добавляем аргументы командной строки """
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox"], help="Выбор браузера")
    parser.addoption("--headless", action="store_true", help="Запуск в headless-режиме")


@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    """ 🔥 Переопределяем логгер перед тестами (если нужно) """
    global log_instance
    log_instance = Logger(log_file="../logs/debug_log.log", level="INFO").get_logger()

@pytest.fixture(scope="session")
def driver(request):
    """ Фикстура для Selenium WebDriver """
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

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Делаем скриншот при падении теста """
    outcome = yield
    report = outcome.get_result()
    if report.failed and "driver" in item.funcargs:
        driver = item.funcargs["driver"]
        driver.save_screenshot(f"screenshots/{item.name}.png")

