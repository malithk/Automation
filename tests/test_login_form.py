import pytest
from pages.login_page import LoginPage
from utils.data_reader import read_login_test_data

@pytest.mark.parametrize("username, password, expected_msg_part", read_login_test_data())
def test_login_form_csv(setup, username, password, expected_msg_part):
    login_page = LoginPage(setup)
    login_page.load()
    login_page.login(username, password)

    message = login_page.get_message()
    assert expected_msg_part in message