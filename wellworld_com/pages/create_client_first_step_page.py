from pylenium.driver import Pylenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys, ActionChains

from wellworld_com.pages.page_base import PageBase


class CreateClientFirstStep(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def set_form(self, first_name, last_name, email, phone, gender, birthday, height: tuple, weight):
        self.py.get("[id='firstName']").type(first_name)
        self.py.get("[id='lastName']").type(last_name)
        self.py.get("[id='email']").type(email)
        self.py.get("[id='mobilePhone']").type(phone)
        self.py.get("[id='practitioner']").select_by_index(1)   # Select the first value on dropdown
        self.py.get("[id='gender']").select_by_text(gender)

        # Set birthday
        ActionChains(self.py.webdriver).send_keys(Keys.TAB).perform()
        ActionChains(self.py.webdriver).send_keys(birthday[0]).perform()  # Set day
        ActionChains(self.py.webdriver).send_keys(birthday[1]).perform()  # Set month
        ActionChains(self.py.webdriver).send_keys(birthday[2]).perform()  # Set year

        self.py.get("[id='heightFeetAndCm']").type(str(height[0]))
        self.py.get("[id='heightInch']").type(str(height[1]))
        self.py.get("[id='weight']").type(str(weight))

    def press_create_without_program_button(self):
        self.py.findx("//button[@id='createWithoutProgram']").first().click()
        element = self.py.wait().\
            until(EC.element_to_be_clickable((By.XPATH, "//div[@id='confirmationPopup']//div[text()='Yes, Create']")))
        element.click()

    def press_next_button(self):
        self.py.get("[type='submit']").click()
