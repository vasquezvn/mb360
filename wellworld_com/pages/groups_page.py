from pylenium.driver import Pylenium
from selenium.webdriver import Keys, ActionChains

from wellworld_com.pages.page_base import PageBase


class GroupsPage(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def press_add_group_button(self):
        self.py.get("a[href='/group/create']").click()

    def set_add_group_form(self, group_name, plan_name, start_date: list):
        self.py.get("#name").type(group_name)
        self.py.get("#practitionerId").select_by_index(1)
        self.py.get("#planId").select_by_text(plan_name)

        # Set Start Date
        ActionChains(self.py.webdriver).send_keys(Keys.TAB).perform()
        ActionChains(self.py.webdriver).send_keys(start_date[0]).perform()  # Set day
        ActionChains(self.py.webdriver).send_keys(start_date[1]).perform()  # Set month
        ActionChains(self.py.webdriver).send_keys(start_date[2]).perform()  # Set year

    def press_create_group_button(self):
        self.py.get("#buttonSubmit").click()

    def search_group(self, query):
        self.py.findx("//input[@id='group.name']").first().type(query, Keys.ENTER)
