from pylenium.driver import Pylenium
from selenium.webdriver.common.by import By

from wellworld_com.pages.page_base import PageBase


class CreateClientThirdStep(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def press_submit_button(self):
        self.py.scroll_to(0, 200)
        self.py.wait(5, use_py=True).until(lambda x: x.find_element(By.ID, "Submit").is_displayed())
        self.py.get("[id='Submit']").click()
