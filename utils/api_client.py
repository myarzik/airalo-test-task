import requests
import allure
from utils.logger import log_instance

class APIClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    @allure.step('Authenticate and obtain access token')
    def authenticate(self):
        """ Retrieves an OAuth2 access token """
        url = f'{self.base_url}/v2/token'
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }

        log_instance.info(f'Authenticating API client at {url}')
        response = self._send_request('POST', url, headers=headers, data=data)
        self.token = response.get('data', {}).get('access_token')

        if self.token:
            log_instance.info('Authentication successful')
            allure.attach(self.token, name='Access Token', attachment_type=allure.attachment_type.TEXT)
        else:
            log_instance.error('Authentication failed: No access token received')
            raise Exception('Authentication failed')

    @allure.step('Submit an eSIM order')
    def submit_order(self, package_id, quantity=1, description=None, brand_settings_name=None):
        """ Submits an eSIM order """
        url = f'{self.base_url}/v2/orders'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
        payload = {
            'quantity': quantity,
            'package_id': package_id,
            'type': 'sim',
            'description': description or 'Default order description',
            'brand_settings_name': brand_settings_name or 'our perfect brand'
        }

        log_instance.info(f'Submitting order: {payload}')
        allure.attach(str(payload), name='Order Payload', attachment_type=allure.attachment_type.JSON)
        return self._send_request('POST', url, headers=headers, json=payload)

    @allure.step('Retrieve eSIMs list')
    def get_esims(self, limit=100, page=1, iccid=None):
        """ Fetches a list of eSIMs """
        url = f'{self.base_url}/v2/sims'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json'
        }
        params = {'limit': limit, 'page': page}
        if iccid:
            params['filter[iccid]'] = iccid

        log_instance.info(f'Fetching eSIMs with params: {params}')
        allure.attach(str(params), name='Query Params', attachment_type=allure.attachment_type.TEXT)
        return self._send_request('GET', url, headers=headers, params=params)

    def _send_request(self, method, url, headers=None, json=None, data=None, params=None):
        """ Helper method for sending API requests with logging """
        try:
            log_instance.info(f'Sending {method} request to {url}')
            if json:
                log_instance.info(f'Payload: {json}')
                allure.attach(str(json), name='Request Payload', attachment_type=allure.attachment_type.JSON)
            if data:
                log_instance.info(f'Form Data: {data}')
            if params:
                log_instance.info(f'Params: {params}')

            response = requests.request(method, url, headers=headers, json=json, data=data, params=params)
            response.raise_for_status()
            log_instance.info(f'Response: {response.status_code} {response.reason}')
            allure.attach(str(response.json()), name='Response', attachment_type=allure.attachment_type.JSON)

            return response
        except requests.exceptions.RequestException as e:
            log_instance.error(f'API request failed: {e}')
            if response is not None:
                log_instance.error(f'Response Body: {response.text}')
                allure.attach(response.text, name='Error Response', attachment_type=allure.attachment_type.TEXT)
            raise
