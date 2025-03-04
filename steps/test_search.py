import allure
from pytest_bdd import given, when, then, parsers, scenarios
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.popup_page import PopupPage

scenarios('../features/search_japan.feature')


@given('the user opens the Airalo homepage')
@allure.step('Opening Airalo homepage')
def open_homepage(driver):
    home_page = HomePage(driver)
    home_page.open_url('https://www.airalo.com/')


@when(parsers.parse('the user searches for "{country}"'))
@allure.step('Searching for country: {country}')
def search_for_country(driver, country):
    home_page = HomePage(driver)
    home_page.search_for_country(country)


@when('selects the first paid eSIM package')
@allure.step('Selecting the first paid eSIM package')
def select_first_paid_package(driver):
    search_page = SearchPage(driver)
    search_page.click_first_paid_package()


@then(parsers.parse('the package {key} should be "{expected_value}"'))
@allure.step('Verifying package {key} should be "{expected_value}"')
def check_package_detail(driver, key, expected_value):
    popup_page = PopupPage(driver)

    assert key in popup_page.LOCATORS, f'Error: key "{key}" not found in LOCATORS!'

    actual_value = popup_page.get_text_from_locator(key)

    assert actual_value == expected_value, f'Error: {key} expected "{expected_value}", but got "{actual_value}"'
