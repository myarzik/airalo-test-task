import allure


@allure.feature('Authentication')
@allure.story('Verify API authentication')
def test_authentication(api_client):
    """ Tests if API authentication is successful """
    with allure.step('Check if authentication token is received'):
        assert api_client.token, 'Authentication failed, token is None'


@allure.feature('eSIM Management')
@allure.story('Retrieve eSIMs list')
def test_get_esims(api_client):
    """ Tests retrieval of eSIMs list """
    with allure.step('Send request to fetch eSIMs'):
        response = api_client.get_esims(limit=10, page=1)

    with allure.step('Validate response status code'):
        assert response.status_code == 200, f'Unexpected status code: {response.status_code}'

    with allure.step('Check response contains eSIM data'):
        json_data = response.json()
        assert 'data' in json_data, 'Response does not contain "data"'


@allure.feature('Order Management')
@allure.story('Submit an eSIM order')
def test_submit_order(api_client):
    """ Tests submitting an eSIM order """
    package_id = 'kallur-digital-7days-1gb'

    with allure.step(f'Send request to submit order for package {package_id}'):
        response = api_client.submit_order(package_id=package_id)

    with allure.step('Validate response status code'):
        assert response.status_code == 200, f'Unexpected status code: {response.status_code}'

    with allure.step('Check response contains correct package ID'):
        json_data = response.json()
        assert json_data.get('data', {}).get('package_id') == package_id, 'Package ID does not match'
