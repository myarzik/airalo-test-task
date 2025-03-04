from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class PopupPage(BasePage):
    """ Represents the popup containing eSIM details """

    LOCATORS = {
        'POPUP': (By.XPATH, '//div[@data-testid="package-detail"]'),
        'SELECTED_SIM': (By.XPATH, '//div[@data-testid="sim-detail-header"]'),
        'PACKAGE_TITLE': (By.XPATH, '//div[@data-testid="package-detail"]//div[@data-testid="sim-detail-operator-title"]'),
        'COVERAGE': (By.XPATH, '//div[@data-testid="package-detail"]//p[@data-testid="COVERAGE-value"]'),
        'DATA': (By.XPATH, '//div[@data-testid="package-detail"]//p[@data-testid="DATA-value"]'),
        'VALIDITY': (By.XPATH, '//div[@data-testid="package-detail"]//p[@data-testid="VALIDITY-value"]'),
        'PRICE': (By.XPATH, '//div[@data-testid="package-detail"]//p[@data-testid="PRICE-value"]'),
    }

    def get_text_from_locator(self, key):
        """ Retrieves text from an element by its key """
        if key not in self.LOCATORS:
            raise ValueError(f'Error: Locator {key} not found!')

        self.wait_for_element(self.LOCATORS['POPUP'])
        self.wait_for_element(self.LOCATORS['SELECTED_SIM'])
        self.wait.until(EC.text_to_be_present_in_element(self.LOCATORS[key], ''))

        return self.get_text(self.LOCATORS[key])
