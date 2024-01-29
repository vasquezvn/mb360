from random import randint
from random import choice
from datetime import datetime

############################################################
#                   AUX METHODS
############################################################


def _generate_suppl_list(py, num_suppl):
    """Method to generate a list of dictionaries that contains main characteristics of
    supplements.
    :param py: Pylenium driver
    :param num_suppl: Number of supplements generated
    :return: List of dictionaries that contain supplement info:
        * suppl_name
        * suppl_dose
        * suppl_measure
    """
    suppl_list = []

    for _ in range(num_suppl):
        suppl_list.append(
            dict(suppl_name=f"suppl_{py.fake.uuid4(cast_to=str).split('-')[0]}",
                 suppl_dose=str(randint(1, 5)),
                 suppl_measure=choice(["g", "mL", "Bar(s)", "Drop(s)"])))

    return suppl_list


def _generate_client_data(py):
    """Generate required data to create client
    :param py: Pylenium driver
    :return: Return a dictionary with required data to create client:
        * name
        * lastname
        * email
        * phone
        * gender
        * birthday
        * height
        * weight
    """
    name = py.fake.first_name()
    lastname = py.fake.last_name()

    # random data to birthday
    day = randint(1, 28)
    month = randint(1, 12)
    year = randint(1990, 2000)

    # random data to Height
    feet = randint(3, 6)
    inches = randint(0, 10)

    return {'name': name,
            'lastname': lastname,
            'email': f"{name.lower()}.{lastname.lower()}@example.org",
            'phone': py.fake.msisdn()[3:],
            'gender': choice(["Female", "Male", "Non-binary", "Other"]),
            'birthday': [day, month, year],
            'height': (feet, inches),
            'weight': randint(150, 190)}


def _get_plan():
    """ Get Plan name randomly

    :return: plan name randomly as str.
    """
    return choice(["10 Day Reset Cleanse",
                   "Adrenal Support Cleanse - 14 Days",
                   "Adrenal Support Cleanse - 28 Days",
                   "Anti-Candida Diet - 28 Days",
                   "Auto Immune Paleo Reset - 28 Days",
                   "Clean Eating Challenge - 14 Days",
                   "Clean Eating Challenge - 28 Days",
                   "Elimination Diet - 21 Days",
                   "Elimination Diet - 28 Days",
                   "Elimination Vegan Diet - 21-Day",
                   "Endocannabinoid Support - 14 Days",
                   "Endocannabinoid Support - 28 Days",
                   "Food Diary - 14 Days",
                   "Food Diary - 30 Days"])


def _get_body_metrics():
    """generate a list of strings with name of body metrics that they can be included multiple times

    :return: List of strings with available body metrics can be record multiple times
    """
    body_metrics = []

    for _ in range(1, 16):
        body_metrics.append(choice(["sleep", "weight", "pain_index", "meditation",
                                    "elimination", "waist", "blood_ketones", "quick_track_fluids",
                                    "blood_pressure", "body_fat_index", "urine_ph", "intermittent_fasting",
                                    "blood_sugar", "temperature", "heart_rate_variability"]))

    return body_metrics


############################################################
#                   TEST METHODS
############################################################


def test_add_client_without_program(py, login_web, well_world):
    dict_client_data = _generate_client_data(py)

    well_world.header.goto_clients()
    well_world.clients.press_add_button()

    well_world.create_client_first_step.set_form(dict_client_data['name'],
                                                 dict_client_data['lastname'],
                                                 dict_client_data['email'],
                                                 dict_client_data['phone'],
                                                 dict_client_data['gender'],
                                                 dict_client_data['birthday'],
                                                 dict_client_data['height'],
                                                 dict_client_data['weight'])

    well_world.create_client_first_step.press_create_without_program_button()
    well_world.clients.search(dict_client_data['email'])
    well_world.clients.goto_client_profile()

    assert py.contains(dict_client_data['name'])
    assert py.contains(dict_client_data['lastname'])
    assert py.contains(dict_client_data['email'])
    assert py.contains(dict_client_data['gender'])


def test_add_client_with_diet_plan(py, login_web, well_world):
    dict_client_data = _generate_client_data(py)

    well_world.header.goto_clients()
    well_world.clients.press_add_button()

    well_world.create_client_first_step.set_form(dict_client_data['name'],
                                                 dict_client_data['lastname'],
                                                 dict_client_data['email'],
                                                 dict_client_data['phone'],
                                                 dict_client_data['gender'],
                                                 dict_client_data['birthday'],
                                                 dict_client_data['height'],
                                                 dict_client_data['weight'])

    well_world.create_client_first_step.press_next_button()
    well_world.create_client_second_step.set_diet_plan()
    well_world.create_client_second_step.press_next_button()
    well_world.create_client_third_step.press_submit_button()

    well_world.clients.search(dict_client_data['email'])
    well_world.clients.goto_client_profile()

    assert py.contains(dict_client_data['name'])
    assert py.contains(dict_client_data['lastname'])
    assert py.contains(dict_client_data['email'])
    assert py.contains(dict_client_data['gender'])
    assert py.contains("Active")


def test_add_client_with_group_plan(py, login_web, well_world):
    plan_name = _get_plan()
    group_name = f"group_{py.fake.uuid4(cast_to=str).split('-')[0]}"
    dict_client_data = _generate_client_data(py)
    start_date = datetime.today().strftime('%d-%m-%Y').split('-')

    # Create group
    well_world.header.goto_groups()
    well_world.groups.press_add_group_button()
    well_world.groups.set_add_group_form(group_name, plan_name, start_date)
    well_world.groups.press_create_group_button()
    well_world.groups.search_group(group_name)

    assert py.should().not_contain("There are no groups to show")

    # Assign group created
    well_world.header.goto_clients()
    well_world.clients.press_add_button()
    well_world.create_client_first_step.set_form(dict_client_data['name'],
                                                 dict_client_data['lastname'],
                                                 dict_client_data['email'],
                                                 dict_client_data['phone'],
                                                 dict_client_data['gender'],
                                                 dict_client_data['birthday'],
                                                 dict_client_data['height'],
                                                 dict_client_data['weight'])

    well_world.create_client_first_step.press_next_button()
    well_world.create_client_second_step.set_group_plan(group_name)
    well_world.create_client_second_step.press_next_button()
    well_world.create_client_third_step.press_submit_button()

    well_world.clients.search(dict_client_data['email'])
    well_world.clients.goto_client_profile()

    assert py.contains(dict_client_data['name'])
    assert py.contains(dict_client_data['lastname'])
    assert py.contains(dict_client_data['email'])
    assert py.contains(dict_client_data['gender'])
    assert py.contains(group_name)


def test_add_client_with_suppl_plan(py, login_web, well_world):
    dict_client_data = _generate_client_data(py)

    well_world.header.goto_clients()
    well_world.clients.press_add_button()

    well_world.create_client_first_step.set_form(dict_client_data['name'],
                                                 dict_client_data['lastname'],
                                                 dict_client_data['email'],
                                                 dict_client_data['phone'],
                                                 dict_client_data['gender'],
                                                 dict_client_data['birthday'],
                                                 dict_client_data['height'],
                                                 dict_client_data['weight'])

    well_world.create_client_first_step.press_next_button()
    well_world.create_client_second_step.set_suppl_plan()
    well_world.create_client_second_step.press_next_button()
    well_world.create_client_third_step.press_submit_button()

    well_world.clients.search(dict_client_data['email'])
    well_world.clients.goto_client_profile()

    assert py.contains(dict_client_data['name'])
    assert py.contains(dict_client_data['lastname'])
    assert py.contains(dict_client_data['email'])
    assert py.contains(dict_client_data['gender'])


def test_db_connection(py, db_connection):
    json_connection = db_connection

    assert len(json_connection) == 0


def test_db_create_patient(py, create_patient):
    response_create_patient = create_patient

    assert len(response_create_patient) != 0


def test_edit_client(py, login_web, well_world, create_patient):
    dict_patient = create_patient
    dict_client_data = _generate_client_data(py)

    well_world.header.goto_clients()
    well_world.clients.search(dict_patient["email"])
    well_world.clients.goto_client_profile()
    well_world.client_detail.press_edit_button()

    well_world.client_detail.set_edit_client_form(
        dict_client_data["name"],
        dict_client_data["lastname"],
        dict_client_data["email"],
        dict_client_data["phone"],
        dict_client_data["gender"],
        dict_client_data["birthday"],
        dict_client_data["height"],
        dict_client_data["weight"]
    )
    well_world.client_detail.press_save_client_form()

    assert py.contains(dict_client_data['name'])
    assert py.contains(dict_client_data['lastname'])
    assert py.contains(dict_client_data['email'])
    assert py.contains(dict_client_data['gender'])


def test_note_client_profile(py, login_web, well_world, create_patient):
    dict_patient = create_patient
    text_note = py.fake.paragraph(nb_sentences=5)
    text_note2 = py.fake.paragraph(nb_sentences=5)

    well_world.header.goto_clients()
    well_world.clients.search(dict_patient["email"])
    well_world.clients.goto_client_profile()

    # Add note
    well_world.client_detail.press_add_note_button()
    well_world.client_detail.set_note(text_note)
    well_world.client_detail.press_save_note_button()
    assert py.contains(text_note[:30])

    # Edit note
    well_world.client_detail.click_edit_note_icon()
    well_world.client_detail.clear_text_note()
    well_world.client_detail.set_note(text_note2)
    well_world.client_detail.press_save_note_button()
    assert py.contains(text_note2[:30])

    # Delete note
    well_world.client_detail.click_delete_note_icon()
    well_world.client_detail.press_confirm_delete_note_button()
    assert py.contains("There are no notes yet")


def test_add_diet_sequence_plans_body_metrics(py, login_web, well_world, create_patient):
    dict_patient = create_patient
    plan_name = _get_plan()
    seq_plan_name = _get_plan()
    body_metrics = _get_body_metrics()

    well_world.header.goto_clients()
    well_world.clients.search(dict_patient["email"])
    well_world.clients.goto_client_profile()

    # Test Add Plan
    well_world.client_detail.press_add_plan_button()
    well_world.client_detail.set_add_diet_plan(plan_name, body_metrics)
    well_world.client_detail.press_next_button_add_plan_form()
    well_world.client_detail.press_save_button_add_plan_form()

    py.scroll_to(0, 100)
    assert py.contains(plan_name)

    # Test Add Sequence Plan
    well_world.client_detail.press_add_plan_button()
    well_world.client_detail.set_add_diet_plan(seq_plan_name, body_metrics)
    well_world.client_detail.press_next_button_add_plan_form()
    well_world.client_detail.press_save_button_add_plan_form()

    py.scroll_to(0, 100)
    assert py.contains(seq_plan_name)

    # Validate body metrics
    selected_body_metric = well_world.client_detail.get_body_metrics()
    b_metrics_match = True

    for b_metric in body_metrics:
        if b_metric not in selected_body_metric:
            b_metrics_match = False
            break

    assert b_metrics_match is True


def test_add_group_plan(py, login_web, well_world, create_patient):
    dict_patient = create_patient
    plan_name = _get_plan()
    group_name = f"group_{py.fake.uuid4(cast_to=str).split('-')[0]}"
    start_date = datetime.today().strftime('%d-%m-%Y').split('-')

    # Create group
    well_world.header.goto_groups()
    well_world.groups.press_add_group_button()
    well_world.groups.set_add_group_form(group_name, plan_name, start_date)
    well_world.groups.press_create_group_button()
    well_world.groups.search_group(group_name)

    assert py.should().not_contain("There are no groups to show")

    well_world.header.goto_clients()
    well_world.clients.search(dict_patient["email"])
    well_world.clients.goto_client_profile()

    # Assign group plan
    well_world.client_detail.press_add_plan_button()
    well_world.client_detail.set_group_plan(group_name)
    well_world.client_detail.press_next_button_add_plan_form()
    well_world.client_detail.press_save_button_add_plan_form()

    assert py.contains(group_name)
    py.scroll_to(0, 100)
    assert py.contains(plan_name)


def test_add_suppl_only_plan_assigned_suppl(py, login_web, well_world, create_patient):
    dict_patient = create_patient
    suppl_list = _generate_suppl_list(py, randint(1, 3))

    well_world.header.goto_clients()
    well_world.clients.search(dict_patient["email"])
    well_world.clients.goto_client_profile()

    # Add supplements
    well_world.client_detail.press_add_plan_button()
    well_world.client_detail.set_supplements_only_plan(suppl_list)
    well_world.client_detail.press_next_button_add_plan_form()
    well_world.client_detail.press_save_button_add_plan_form()

    assert py.contains("Supplements assigned successfully")

    # Validate supplements included on plan
    assigned_suppl_list = well_world.client_detail.get_assigned_suppl()
    suppl_match = True

    for suppl_assigned in suppl_list:
        if suppl_assigned["suppl_name"] not in assigned_suppl_list:
            suppl_match = False
            break

    assert suppl_match is True
