from pylenium.driver import Pylenium


class HeaderNav:
    def __init__(self, py: Pylenium):
        self.py = py

    def goto_home(self):
        self.py.get("a[href='practitionerProfile/index']").click()

    def goto_clients(self):
        self.py.findx("//nav[@id='app-header']//ul[@class='nav nav-tabs hidden-xs']/li[2]").first().click()

    def goto_groups(self):
        self.py.findx("//nav[@id='app-header']/ul[@class='nav nav-tabs hidden-xs']/li[3]").first().click()

    def logout(self):
        self.py.get("[id='avatar-item']").click()
        self.py.get("a[href='/logout/index']").click()
