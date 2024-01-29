from pylenium.driver import Pylenium
from selenium.webdriver import Keys

from wellworld_com.pages.page_base import PageBase


class HomePage(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def log_out(self):
        self.header.logout()

    def search(self, query: str):
        self.py.get("[id='searchTerm']").type(query, Keys.ENTER)
