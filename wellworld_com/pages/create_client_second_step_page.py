from random import randint

from pylenium.driver import Pylenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from wellworld_com.pages.page_base import PageBase


class CreateClientSecondStep(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def set_diet_plan(self):
        self.py.get("[id='planId']").select_by_index(randint(1, 40))

    def set_group_plan(self, group_name):
        self.py.get("[id='programOption']").select_by_value("GROUP")
        self.py.get("[id='groupId']").select_by_text(group_name)

    def set_suppl_plan(self):
        self.py.get("[id='programOption']").select_by_value("SUPPLEMENTS_ONLY")

        self.py.get("[id='add-supplement-btn']").click()

        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "supName")))
        element.send_keys("Test Suppl 1")

        self.py.get("[id='supDosageQuantity']").type(str(randint(1, 10)))
        self.py.get("[id='supDosage']").select_by_index(randint(1,16))
        self.py.findx("//form[@id='offSearchForm']//button[@class='multiselect dropdown-toggle btn btn-default']").\
            first().click()
        self.py.findx("//form[@id='offSearchForm']//ul[@class='multiselect-container dropdown-menu']/li[5]").\
            first().click()
        self.py.findx("//form[@id='offSearchForm']//button[@class='btn btn-primary col-lg-2 col-lg-offset-8']").\
            first().click()

    def press_next_button(self):
        self.py.execute_script("arguments[0].click();",self.py.wait().
                               until(EC.element_to_be_clickable((By.XPATH, "//button[@id='nextButton']"))))
