from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log_instance  # Importing logger

class SearchPage(BasePage):
    """ Represents the search results page for eSIM packages """

    LOCATORS = {
        'PAID_PACKAGES': (By.XPATH, "//a[@data-testid='sim-package-item'][not(descendant::button[contains(text(), 'GET FREE eSIM')]) and descendant::button[contains(text(), 'BUY NOW')]]"),
        'BUY_NOW_BUTTON': (By.CSS_SELECTOR, 'div[data-testid="esim-button"]'),
    }

    def get_paid_packages(self):
        """ Finds all available paid eSIM packages on the page """
        self.wait_for_element(self.LOCATORS['PAID_PACKAGES'])
        return self.driver.find_elements(*self.LOCATORS['PAID_PACKAGES'])

    def click_first_paid_package(self):
        """ Clicks the 'BUY NOW' button on the first available paid eSIM package """
        packages = self.get_paid_packages()
        if packages:
            log_instance.info(f"Found {len(packages)} paid eSIMs. Selecting the first one.")
            buy_now_button = packages[0].find_element(*self.LOCATORS['BUY_NOW_BUTTON'])
            self.click(buy_now_button)
        else:
            log_instance.error("No paid eSIM packages found!")
            raise Exception("No available paid eSIMs")
