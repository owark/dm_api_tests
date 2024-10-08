import time
import structlog
from hamcrest import assert_that, has_properties
from dm_api_account.models.user_envelope_model import UserRole
from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def test_post_v1_account_login():
    api = Facade(host="http://5.63.153.31:5051")
    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')

    login = 'login_test000035'
    email = 'login_test000035@gmail.com'
    password = 'password01'

    db.delete_user_by_login(login=login)
    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'
        assert len(dataset) == 0
    time.sleep(2)

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} not registered'
        assert row['Activated'] is False, f'User {login} was activated'

    api.account.activate_registered_user(
        login=login
    )
    time.sleep(2)

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Activated'] is True, f'User {login} not activated'

    response = api.login.login_user(
        login=login,
        password=password
    )

    assert_that(response.resource, has_properties(
        {
            "login": login,
            "roles": [UserRole.guest, UserRole.player],
            "medium_picture_url": None,
            "small_picture_url": None,
            "status": None
        }
    ))
    assert response.status_code == 201, f'Статус кода ответа должен быть равен 201, но он равен {response.status_code}'