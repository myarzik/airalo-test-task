from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.popup_page import PopupPage
from pytest_bdd import given, when, then, parsers, scenarios

@given("the user opens the Airalo homepage")
def open_homepage(driver):
    home_page = HomePage(driver)
    home_page.open_url("https://www.airalo.com/")

@when('the user searches for "Japan"')
def search_for_japan(driver):
    home_page = HomePage(driver)
    home_page.search_for_country("Japan")

@when("selects the first paid eSIM package")
def select_first_paid_package(driver):
    search_page = SearchPage(driver)
    search_page.click_first_paid_package()

@then(parsers.parse('the package {key} should be "{expected_value}"'))
def check_package_detail(driver, key, expected_value):
    popup_page = PopupPage(driver)

    # Проверяем, что ключ существует в LOCATORS
    assert key in popup_page.LOCATORS, f"❌ Ошибка: ключ '{key}' отсутствует в LOCATORS!"

    # Получаем фактическое значение с UI
    actual_value = popup_page.get_text_from_locator(key)

    # Сравниваем фактическое значение с ожидаемым
    assert actual_value == expected_value, f"❌ {key}: ожидалось '{expected_value}', получено '{actual_value}'"
    print(f"✅ {key} верное: '{actual_value}'")

scenarios('../features/search_japan.feature')