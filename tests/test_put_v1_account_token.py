import time
import structlog
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_put_v1_account_token():
    api = DmApiAccount(host="http://5.63.153.31:5051")
    mailhog = MailHogApi(host="http://5.63.153.31:5025")
    json = RegistrationModel(
        login="login366",
        email="email366@ru",
        password="password35"
    )
    api.account.post_v1_account(json=json)
    time.sleep(2)
    token = mailhog.get_token_from_the_last_email()
    response = api.account.put_v1_account_token(token=token)
    assert response.status_code == 200, f'Статус кода ответа должен быть равен 201, но он равен {response.status_code}'
