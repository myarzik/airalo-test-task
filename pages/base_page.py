from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.logger import log_instance  # Импортируем логгер

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def safe_execute(self, action, *args, **kwargs):
        """ 🔥 Обёртка для методов, чтобы логировать ошибки """
        try:
            return action(*args, **kwargs)
        except Exception as e:
            log_instance.error(f"❌ Ошибка в методе {action.__name__}: {e}")
            self.save_screenshot(action.__name__)  # Сохраняем скриншот
            raise e  # Пробрасываем ошибку дальше

    def save_screenshot(self, method_name):
        """ Сохраняет скриншот при ошибке """
        screenshot_path = f"screenshots/{method_name}.png"
        self.driver.save_screenshot(screenshot_path)
        log_instance.error(f"📸 Скриншот ошибки сохранён: {screenshot_path}")

    def open_url(self, url):
        """ Открывает страницу и принимает куки, если попап появился """
        log_instance.info(f"Открываем страницу: {url}")
        self.safe_execute(self.driver.get, url)
        self.accept_cookies()  # 🔥 Автоматически закрываем попап
        self.decline_notifications()

    def click(self, locator):
        """ Кликает на элемент """
        log_instance.info(f"Кликаем на элемент: {locator}")
        self.safe_execute(self.wait.until(EC.element_to_be_clickable(locator)).click)

    def fill(self, locator, text):
        """ Вводит текст в поле """
        log_instance.info(f"Вводим '{text}' в поле {locator}")
        self.safe_execute(self.wait.until(EC.presence_of_element_located(locator)).send_keys, text)

    def wait_for_element(self, locator):
        """ Ждёт появления элемента """
        log_instance.info(f"Ожидаем появления элемента: {locator}")
        return self.safe_execute(self.wait.until, EC.presence_of_element_located(locator))

    def get_text(self, locator):
        """ 🔥 Возвращает текст элемента, если он найден """
        element = self.wait.until(EC.presence_of_element_located(locator))
        text = element.text.strip()
        log_instance.info(f"🔹 Получен текст {locator}: '{text}'")
        return text

    def accept_cookies(self):
        """ 🔥 Закрывает попап с куками, если он есть """
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            log_instance.info("🟢 Обнаружен попап с куками, закрываем его")
            cookie_button.click()
        except:
            log_instance.info("✅ Попап с куками не найден, продолжаем тест")

    def decline_notifications(self):
        """ 🔥 Закрывает попап с куками, если он есть """
        try:
            forbid_notifications_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "wzrk-cancel"))
            )
            log_instance.info("🟢 Обнаружен попап с уведомлениями, закрываем его")
            forbid_notifications_button.click()
        except:
            log_instance.info("✅ Попап с уведомлениями не найден, продолжаем тест")