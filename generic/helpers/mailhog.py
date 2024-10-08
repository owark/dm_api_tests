import json
import time

from requests import Response
from restclient.restclient import RestClient


def decorator(fn):
    def wrapper(*args, **kwargs):
        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']
            if len(emails) < 1:
                print(f'attempt {i}')
                time.sleep(2)
                continue
            else:
                return response

    return wrapper


class MailhogApi:
    def __init__(self, host="http://5.63.153.31:5025"):
        self.host = host
        self.client = RestClient(host=host)

    @decorator
    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """

        response = self.client.get(
            path="/api/v2/messages",
            params={
                "limit": limit
            }
        )
        return response

    def get_token_from_the_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """

        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        token = token_url.split('/')[-1]
        return token

    def get_token_by_login(self, login: str, attempt=5):
        if attempt == 0:
            raise AssertionError(f'Не удалось получить письмо с логином {login}')
        emails = self.get_api_v2_messages(limit=1).json()['items']
        for email in emails:
            user_data = json.loads(email['Content']['Body'])
            if login == user_data.get('Login'):
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                return token
        time.sleep(2)
        print('Попытка получить письмо')
        return self.get_token_by_login(login=login, attempt=attempt - 1)


if __name__ == '__main__':
    MailhogApi().get_api_v2_messages(limit=50)
