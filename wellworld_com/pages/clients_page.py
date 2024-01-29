from pylenium.driver import Pylenium
from selenium.webdriver import Keys

from wellworld_com.pages.page_base import PageBase


class ClientsPage(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def press_add_button(self):
        self.py.get("a[href='/newClient/firstStep']").click()

    def search(self, query: str):
        self.py.get("[id='searchTerm']").type(query, Keys.ENTER)

    def goto_client_profile(self):
        self.py.findx("//div[@id='tableContent']//td/a").first().click()

