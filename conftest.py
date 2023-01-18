from databases.database_connections import DataBaseConnections
from databases.database_customer_api import DataBaseCustomerApi
from databases.database_tracking_api import DataBaseTrackingApi
from fixture.application import Application
from dotenv import load_dotenv, find_dotenv
import pytest
import os


load_dotenv(find_dotenv())
session = None


@pytest.fixture(scope='session')
def token():
    global session
    """Функция для получения токена для работы по API"""
    data = f"grant_type=client_credentials&client_id={os.getenv('CLIENT_ID')}&client_secret={os.getenv('CLIENT_SECRET')}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    session = Application()
    response = session.open_session(url=f"{os.getenv('URL')}{'/auth/access_token'}", data=data, headers=headers)
    body = response.json()
    token = {
        "Authorization": f"Bearer {body['access_token']}",
        "Content-Type": "application/json"
    }
    return token


@pytest.fixture(scope="session")
def customer_api(request):
    """Фикстура для подключения к базе данных 'customer-api'"""
    database_customer = DataBaseCustomerApi(host=os.getenv("HOST"), database=os.getenv("CUSTOMER-API"),
                                            user=os.getenv("CONNECTIONS"), password=os.getenv("DATABASE_PASSWORD"))
    def fin():
        database_customer.connection_close()
    request.addfinalizer(fin)
    return database_customer


@pytest.fixture(scope="session")
def connections(request):
    """Фикстура для подключения к базе данных 'connections'"""
    database_connections = DataBaseConnections(host=os.getenv("HOST"), database=os.getenv("CONNECTIONS"),
                                               user=os.getenv("CONNECTIONS"), password=os.getenv("DATABASE_PASSWORD"))
    def fin():
        database_connections.connection_close()
    request.addfinalizer(fin)
    return database_connections


@pytest.fixture(scope="session")
def tracking_api(request):
    """Фикстура для подключения к базе данных 'tracking-api'"""
    database_tracking = DataBaseTrackingApi(host=os.getenv("HOST"), database=os.getenv("TRACKING_API"),
                                            user=os.getenv("CONNECTIONS"), password=os.getenv("DATABASE_PASSWORD"))
    def fin():
        database_tracking.connection_close()
    request.addfinalizer(fin)
    return database_tracking


@pytest.fixture(scope="session")
def stop(request, token):
    """Фикстура для завершения сессии"""
    def fin():
        fixture = Application()
        fixture.session_close()
    request.addfinalizer(fin)
