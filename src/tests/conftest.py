from account.models import User

from faker import Faker

import pytest


@pytest.fixture(autouse=True, scope="function")
def enable_db_access_for_all_tests(db):
    """
    give access to database for all tests
    """


@pytest.fixture(scope='function')
def user_fix():
    user = User.objects.create()
    yield user


@pytest.fixture(scope='session')
def fake():
    yield Faker()
