import json
from requests import Response
from restclient.restclient import RestClient


class MailHogApi:
    def __init__(self, host="http://5.63.153.31:5025"):
        self.host = host
        self.client = RestClient(host=host)

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
