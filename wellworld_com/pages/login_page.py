from pylenium.driver import Pylenium


class LoginPage:
    def __init__(self, py: Pylenium):
        self.py = py

    def login(self, user: str, password: str):
        self.py.get("[id='username']").type(user)
        self.py.get("[id='password']").type(password)
        self.py.get("[id='submit']").click()
