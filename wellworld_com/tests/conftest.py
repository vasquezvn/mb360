import uuid

import pytest
import requests
from random import choice

from requests.auth import HTTPBasicAuth

from wellworld_com.pages.header_nav import HeaderNav
from wellworld_com.pages.login_page import LoginPage
from wellworld_com.pages.wellword_pages import WellWorldPages


@pytest.fixture
def db_connection(py):
    auth_payload = _request_payload(py)
    response_test_connection = _get_test_connection(py, auth_payload)
    assert response_test_connection.status_code == 200
    yield response_test_connection.json()


@pytest.fixture
def create_patient(py):
    auth_payload = _request_payload(py)

    name = py.fake.first_name()
    last_name = py.fake.last_name()

    body_payload = {
        "first_name":           name,
        "last_name":            last_name,
        "gender":               choice(["Female", "Male", "Non-binary", "Other"]),
        "plan":                 "bf574865-382e-42ce-80b0-d9609d2cad61",
        "email":                f"{name.lower()}.{last_name.lower()}@example.com",
        "welcome_email_note":   "welcome email note",
        "start_date":           "2024-01-09"
    }

    response_register_client = _post_register_client(py, auth_payload, body_payload)
    assert response_register_client.status_code == 200
    yield response_register_client.json()


@pytest.fixture
def login_web(py):
    py.visit(py.config.custom["qa-environment"]["url"])

    LoginPage(py).login(py.config.custom["qa-environment"]["username"],
                        py.config.custom["qa-environment"]["password"])
    yield
    HeaderNav(py).logout()


@pytest.fixture
def well_world(py):
    return WellWorldPages(py)


# ================================================
#                 TEST API
# ================================================
def _request_payload(py):
    return {
        "username": py.config.custom["api"]["username"],
        "password": py.config.custom["api"]["password"]
    }


def _post_register_client(py, auth_payload, body_payload):
    url = py.config.custom["api"]["base_path"] + "/zapier/registerClient"
    basic = HTTPBasicAuth(auth_payload["username"], auth_payload["password"])
    headers = _get_headers()

    return requests.post(url, auth=basic, headers=headers, json=body_payload)


def _get_test_connection(py, payload):
    basic = HTTPBasicAuth(payload["username"], payload["password"])
    headers = _get_headers()

    return requests.get(py.config.custom["api"]["base_path"] + "/zapier/test", auth=basic, headers=headers)


def _get_headers():
    return {
        "Cookie":           "JSESSIONID=1AB25237F05839B220AFF9C0B6E42E81",
        "Cache-Control":    "no-cache",
        "Postman-Token":    uuid.uuid4().hex,
        "Content-Type":     "application/json",
        "User-Agent":       "PostmanRuntime/7.36.1",
        "Accept":           "*/*",
        "Accept-Encoding":  "gzip, deflate, br",
        "Connection":       "keep-alive"
    }
