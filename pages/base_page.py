from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from utils.logger import log_instance

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def safe_execute(self, action, *args, **kwargs):
        """ Executes an action safely and logs errors """
        try:
            return action(*args, **kwargs)
        except Exception as e:
            log_instance.error(f'Error in method {action.__name__}: {e}')
            self.save_screenshot(action.__name__)
            raise e

    def save_screenshot(self, method_name: str) -> None:
        """ Saves a screenshot in case of an error """
        screenshot_path = f'screenshots/{method_name}.png'
        self.driver.save_screenshot(screenshot_path)
        log_instance.error(f'Screenshot saved: {screenshot_path}')

    def open_url(self, url: str) -> None:
        """ Opens a page and handles popups """
        log_instance.info(f'Opening page: {url}')
        self.safe_execute(self.driver.get, url)
        self.accept_cookies()
        self.decline_notifications()

    def click(self, locator: tuple[str, str]) -> None:
        """ Clicks on an element """
        log_instance.info(f'Clicking on element: {locator}')
        self.safe_execute(self.wait.until(EC.element_to_be_clickable(locator)).click)

    def fill(self, locator: tuple[str, str], text: str) -> None:
        """ Enters text into a field """
        log_instance.info(f'Entering "{text}" into field {locator}')
        self.safe_execute(self.wait.until(EC.presence_of_element_located(locator)).send_keys, text)

    def wait_for_element(self, locator: tuple[str, str]) -> WebElement:
        """ Waits for an element to appear """
        log_instance.info(f'Waiting for element: {locator}')
        return self.safe_execute(self.wait.until, EC.presence_of_element_located(locator))

    def get_text(self, locator: tuple[str, str]) -> str:
        """ Returns the text of an element """
        element = self.wait.until(EC.presence_of_element_located(locator))
        text = element.text.strip()
        log_instance.info(f'Text retrieved {locator}: "{text}"')
        return text

    def accept_cookies(self) -> None:
        """ Closes the cookie popup if present """
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            log_instance.info('Cookie popup detected, closing it')
            cookie_button.click()
        except:
            log_instance.info('Cookie popup not found, continuing test')

    def decline_notifications(self) -> None:
        """ Closes the notification popup if present """
        try:
            forbid_notifications_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, 'wzrk-cancel'))
            )
            log_instance.info('Notification popup detected, closing it')
            forbid_notifications_button.click()
        except:
            log_instance.info('Notification popup not found, continuing test')
