from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-testid="search-input"]')  # 🔥 Новый локатор
    JAPAN_OPTION = (By.XPATH, "//span[@data-testid='Japan-name']")  # 🔥 Обновленный локатор выбора Японии

    def search_for_country(self, country):
        """ 🔥 Вводит название страны в строку поиска и выбирает её из списка """
        self.accept_cookies()  # Убедимся, что попап с куками закрыт
        self.fill(self.SEARCH_INPUT, country)
        self.wait_for_element(self.JAPAN_OPTION)
        self.click(self.JAPAN_OPTION)