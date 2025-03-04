from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log_instance  # 🔥 Импортируем логгер

class SearchPage(BasePage):
    # 🔥 Локатор всех платных eSIM-пакетов (без "FREE WELCOME eSIM", но с "BUY NOW")
    PAID_PACKAGES = (By.XPATH, "//a[@data-testid='sim-package-item'][not(descendant::button[contains(text(), 'GET FREE eSIM')]) and descendant::button[contains(text(), 'BUY NOW')]]")

    # 🔥 Локатор кнопки "BUY NOW" внутри конкретного пакета
    BUY_NOW_BUTTON = (By.CSS_SELECTOR, 'div[data-testid="esim-button"]')

    def get_paid_packages(self):
        """ 🔥 Находит все платные eSIM-пакеты на странице """
        self.wait_for_element(self.PAID_PACKAGES)  # Ждём, пока появятся пакеты
        return self.driver.find_elements(*self.PAID_PACKAGES)  # Возвращаем список пакетов

    def click_first_paid_package(self):
        """ 🔥 Кликает на кнопку 'BUY NOW' в первом платном eSIM-пакете """
        packages = self.get_paid_packages()  # Получаем все платные пакеты
        if packages:
            log_instance.info(f"🔹 Найдено {len(packages)} платных eSIM. Выбираем первый.")
            buy_now_button = packages[0].find_element(*self.BUY_NOW_BUTTON)  # Находим кнопку внутри первого пакета
            self.click(buy_now_button)  # Кликаем "BUY NOW"
        else:
            log_instance.error("❌ Не найдено ни одного платного eSIM-пакета!")
            raise Exception("Нет доступных платных eSIM")