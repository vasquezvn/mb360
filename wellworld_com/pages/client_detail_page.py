from random import randint

from pylenium.driver import Pylenium
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from wellworld_com.pages.page_base import PageBase


class ClientDetailPage(PageBase):
    def __init__(self, py: Pylenium):
        super().__init__(py)

    def press_edit_button(self):
        self.py.get("[id='edit-client-btn']").click()

    def press_add_plan_button(self):
        self.py.get("#add-plan-btn").click()

    def set_add_diet_plan(self, plan_name: str, body_metrics: list):
        self.py.execute_script("arguments[0].click();",self.py.wait().
                               until(EC.element_to_be_clickable((By.ID, "planId"))))

        self.py.get("#planId").select_by_text(plan_name)
        self.py.wait(use_py=True).sleep(3)

        elements = self.py.findx("//div[@id='bodyParametersForPlan']//input[@class='bodyMetricCheckbox']")

        for b_metric in elements:
            if b_metric.get_attribute("value")[1:-1] in body_metrics:
                if not b_metric.is_selected():
                    b_metric.click()
            else:
                if b_metric.is_selected():
                    b_metric.click()

    def press_next_button_add_plan_form(self):
        self.py.wait().until(lambda x: x.find_element(By.ID, "goToSecondStep").is_displayed())

        self.py.execute_script("arguments[0].click();", self.py.wait().
                               until(EC.element_to_be_clickable((By.ID, "goToSecondStep"))))

    def press_save_button_add_plan_form(self):
        self.py.scroll_to(0, 100)
        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "Save")))
        element.click()

    def set_edit_client_form(self, name, lastname, email, phone, gender, birthday, height, weight):
        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "firstName")))
        element.clear()

        self.py.get("#firstName").type(name)

        self.py.get("#lastName").clear()
        self.py.get("#lastName").type(lastname)

        self.py.get("#email").clear()
        self.py.get("#email").type(email)

        self.py.get("#mobilePhone").clear()
        self.py.get("#mobilePhone").type(phone)

        self.py.get("#gender").select_by_value(gender)

        # Set birthday
        ActionChains(self.py.webdriver).send_keys(Keys.TAB).perform()
        ActionChains(self.py.webdriver).send_keys(birthday[0]).perform()  # Set day
        ActionChains(self.py.webdriver).send_keys(birthday[1]).perform()  # Set month
        ActionChains(self.py.webdriver).send_keys(birthday[2]).perform()  # Set year

        self.py.get("#heightFeetAndCm").clear()
        self.py.get("#heightFeetAndCm").type(str(height[0]))

        self.py.get("#heightInch").clear()
        self.py.get("#heightInch").type(str(height[1]))

        self.py.get("#weight").clear()
        self.py.get("#weight").type(str(weight))

    def press_save_client_form(self):
        self.py.get("#buttonSubmit").click()

    def press_add_note_button(self):
        self.py.get("#add-note-btn").click()

    def set_note(self, text_note):
        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "textTrackNote")))
        element.send_keys(text_note)

    def press_save_note_button(self):
        self.py.get("#save-note-btn").click()

    def click_edit_note_icon(self):
        self.py.findx("//span[@class='glyphicon glyphicon-pencil']").first().click()

    def click_delete_note_icon(self):
        self.py.get("[class='glyphicon glyphicon-trash']").click()

    def clear_text_note(self):
        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "textTrackNote")))
        element.clear()

    def press_confirm_delete_note_button(self):
        element = self.py.wait().until(EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-danger']")))
        element.click()

    def set_group_plan(self, group_name):
        self.py.wait().until(lambda x: x.find_element(By.ID, "programOption").is_displayed())
        self.py.get("#programOption").select_by_text("Group")
        self.py.get("#groupId").select_by_text(group_name)

    def set_supplements_only_plan(self, supplements: list):
        element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "programOption")))

        self.py.get("#programOption").select_by_text("Supplements Only - No App Tracking")
        xpath_save_btn = "//form[@id='offSearchForm']//button[@class='btn btn-primary col-lg-2 col-lg-offset-8']"

        for supplement in supplements:
            suppl_freq_xpath = "//form[@id='offSearchForm']" \
                               f"//ul[@class='multiselect-container dropdown-menu']/li[{str(randint(1, 8))}]"

            self.py.get("#newPlanSupplementButton").click()

            element = self.py.wait().until(EC.element_to_be_clickable((By.ID, "supName")))
            element.click()
            self.py.get("#supName").type(supplement["suppl_name"])

            self.py.get("#supDosageQuantity").type(supplement["suppl_dose"])
            self.py.get("#supDosage").select_by_text(supplement["suppl_measure"])
            self.py.findx("//form[@id='offSearchForm']//button[@class='multiselect dropdown-toggle btn btn-default']")\
                .first().click()
            self.py.findx(suppl_freq_xpath).first().click()
            self.py.findx(xpath_save_btn).first().click()

        self.py.wait().until(EC.element_to_be_clickable((By.ID, "supplements-section")))

    def get_body_metrics(self):
        self.py.get("#body-metrics-button").click()
        self.py.wait().until(EC.element_to_be_clickable(
            (By.XPATH, "//form[@id='bodyMetricsForm']//label[@class='option-title']")))

        elements = self.py.findx("//form[@id='bodyMetricsForm']//input[@class='bodyMetricCheckbox']")
        selected_b_metrics = []

        for b_metric in elements:
            if b_metric.is_selected():
                selected_b_metrics.append(b_metric.get_attribute("value")[1:-1])

        self.py.findx("//div[@id='bodyMetricsModal']//button[@class='close']").first().click()

        return selected_b_metrics

    def get_assigned_suppl(self):
        self.py.get("#edit-plan-supplement").click()
        suppl_assigned_list = []

        supplement_elements = self.py.findx("//div[@id='supplement-table-content']//div[@class='prod-title']")

        for e_suppl in supplement_elements:
            suppl_assigned_list.append(e_suppl.text())

        self.py.wait().\
            until(lambda x: x.find_element(By.XPATH, "//div[@id='trackSupplementListPopup']//button[@class='close']").
                  is_displayed())
        self.py.findx("//div[@id='trackSupplementListPopup']//button[@class='close']").first().click()

        return suppl_assigned_list

