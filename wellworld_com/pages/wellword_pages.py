from pylenium.driver import Pylenium

from wellworld_com.pages.client_detail_page import ClientDetailPage
from wellworld_com.pages.clients_page import ClientsPage
from wellworld_com.pages.create_client_first_step_page import CreateClientFirstStep
from wellworld_com.pages.create_client_second_step_page import CreateClientSecondStep
from wellworld_com.pages.create_client_third_step_page import CreateClientThirdStep
from wellworld_com.pages.groups_page import GroupsPage
from wellworld_com.pages.header_nav import HeaderNav
from wellworld_com.pages.home_page import HomePage


class WellWorldPages:
    def __init__(self, py: Pylenium):
        self.header = HeaderNav(py)
        self.home = HomePage(py)
        self.clients = ClientsPage(py)
        self.create_client_first_step = CreateClientFirstStep(py)
        self.create_client_second_step = CreateClientSecondStep(py)
        self.create_client_third_step = CreateClientThirdStep(py)
        self.client_detail = ClientDetailPage(py)
        self.groups = GroupsPage(py)
