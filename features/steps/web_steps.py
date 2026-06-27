from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


ID_MAP = {
    "Search ID": "search_id",
    "Name": "name",
    "Description": "description",
    "Price": "price",
    "Available": "available",
    "Category": "category",
}


@when('I visit the "Home Page"')
def step_impl(context):
    """Visit the application home page."""
    context.driver.get(context.base_url)


@when('I set the "{field}" to "{value}"')
def step_impl(context, field, value):
    """Set an input field value."""
    element_id = ID_MAP[field]
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
def step_impl(context, value, field):
    """Select a value from a dropdown."""
    element_id = ID_MAP[field]
    select = Select(context.driver.find_element(By.ID, element_id))
    select.select_by_visible_text(value)


@when('I press the "{button}" button')
def step_impl(context, button):
    """Press a button by its visible text."""
    xpath = f"//button[contains(., '{button}')]"
    context.driver.find_element(By.XPATH, xpath).click()


@then('I should see "{text}" in the results')
def step_impl(context, text):
    """Check that text appears in the results area."""
    results = context.driver.find_element(By.ID, "search_results")
    assert text in results.text


@then('I should not see "{text}" in the results')
def step_impl(context, text):
    """Check that text does not appear in the results area."""
    results = context.driver.find_element(By.ID, "search_results")
    assert text not in results.text
