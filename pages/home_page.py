from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    LOCATORS = {
        'SEARCH_INPUT': (By.CSS_SELECTOR, 'input[data-testid="search-input"]'),
        'COUNTRY_OPTION': lambda country: (By.XPATH, f"//span[@data-testid='{country}-name']")
    }

    def search_for_country(self, country):
        """ Enters the country name in the search field and selects it from the list """
        self.accept_cookies()
        self.fill(self.LOCATORS['SEARCH_INPUT'], country)
        country_option = self.LOCATORS['COUNTRY_OPTION'](country)
        self.wait_for_element(country_option)
        self.click(country_option)
