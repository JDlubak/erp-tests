from pytest_bdd import parsers, scenarios, when

# BDD-08: powiela UI-10 (tests/ui/test_ts16_logout_ui.py)
scenarios("features/ts16_logout.feature")

PAGE_PATHS = {"sales": "/sales", "home": "/"}


@when(parsers.parse("I try to open the {name} page"))
def try_to_open_page(ui_page, name):
    ui_page.goto(PAGE_PATHS[name])
