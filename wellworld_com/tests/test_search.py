
def test_search_clients_with_active_plan(py, login_web, well_world):
    well_world.home.search("iv024")
    assert py.contains('iv024 tst8')
