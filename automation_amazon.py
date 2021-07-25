from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as cond
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

@allure.story('Testing the process of adding an item on www.amazon.com web page')
class TestClass():

    @allure.description('Setup chrome driver')
    @pytest.fixture(autouse=True)
    def driver(self):
        print("\n  initiating chrome driver")
        driver = webdriver.Chrome(ChromeDriverManager().install())
        print("\n  navigate to https://www.amazon.com/")
        driver.get("https://www.amazon.com/")
        print("\n  maximize the window")
        driver.maximize_window()
        driver.implicitly_wait(5)
        yield driver
        print("\n  close the driver")
        driver.close()

    @allure.title('Create a new user')
    @allure.description('Create a new user and verify that the user exists')
    def test_creation(self, driver):

        self.search_for(driver, "Star Wars")
        self.select_from_dropdown(driver, "Toys & Games")
        self.search_for(driver, "Star Wars")
        self.filter_the_price(driver, 5, 500)

        brands = ["LEGO", "Funko"]
        self.select_brand(driver, brands)
        self.go_to_page(driver, 2)
        item = self.open_product(driver, 1)
        self.select_quantity(driver, 3)
        item_amount = self.get_the_amount(driver)
        expected_subtotal = format(3 * float(item_amount),'.2f')
        self.adding_items(driver)
        self.go_to_cart(driver)
        self.verify_the_item_is_displaying(driver, item)
        self.verify_the_subtotal_amount(driver, expected_subtotal)

    @allure.step('Verify the subtotal amount')
    def verify_the_subtotal_amount(self, driver, expected_subtotal):
        self.page_has_loaded(driver)
        item_amount = re.sub('\$', '', driver.find_element_by_css_selector("#sc-subtotal-amount-activecart > span").text)
        assert expected_subtotal == item_amount
        print("\n  The subtotal amount is correct!")


    @allure.step('Get the item amount')
    def get_the_amount(self, driver):
        item_amount = re.sub('\$','', driver.find_element_by_id("price_inside_buybox").text)
        print("\n  Get an amount: {} of the item.".format(item_amount))
        self.page_has_loaded(driver)
        return item_amount

    @allure.step('Searching for item')
    def search_for(self, driver, input_param):
        search_data = driver.find_element_by_id("twotabsearchtextbox")
        search_data.clear()
        search_data.click()
        search_data.send_keys(input_param)
        print("\n  Searching for {}.".format(input_param))
        self.page_has_loaded(driver)
        driver.find_element_by_id("nav-search-submit-button").click()
        print("\n  Search button was clicked")
        self.page_has_loaded(driver)

    @allure.step('Select from dropdown of the search box')
    def select_from_dropdown(self, driver, input_param):
        search_dropdown_box = driver.find_element_by_id("searchDropdownBox")
        select = Select(search_dropdown_box)
        select.select_by_visible_text(input_param)
        print("\n  Selecting {} from the search dropdown.".format(input_param))
        self.page_has_loaded(driver)

    @allure.step('Verify the item')
    def verify_the_item_is_displaying(self, driver, item):
        if len(driver.find_elements_by_css_selector("span.a-size-medium.a-color-base.sc-product-title")) > 0:
            assert item == driver.find_element_by_css_selector("span.a-size-medium.a-color-base.sc-product-title").text
        else:
            print("There is no items in the cart")
            raise Exception("There is no items in the cart")

    @allure.step('Go to cart')
    def go_to_cart(self, driver):
        driver.find_element_by_id("nav-cart").click()

    @allure.step('Adding items in the cart')
    def adding_items(self, driver):
        if len(driver.find_elements_by_id("add-to-cart-button")) > 0:
            time.sleep(1)
            driver.find_element_by_id("add-to-cart-button").click()
        else:
            print("There is no cart button")
            raise Exception("here is no cart button")

    @allure.step('Open a product')
    def open_product(self, driver, page_number):
        self.page_has_loaded(driver)
        WebDriverWait(driver, 10).until(cond.presence_of_all_elements_located((By.XPATH, '//div[@data-component-id]')))
        WebDriverWait(driver, 10).until(
            cond.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.a-link-normal.a-text-normal')))
        time.sleep(3)
        item = driver.find_elements_by_css_selector("a.a-link-normal.a-text-normal")[page_number - 1]
        item_text = item.text
        item.click()
        print("\n  Go to product: {} ".format(item_text))
        return item_text

    @allure.step('Go to page')
    def go_to_page(self, driver, page_number):
        self.page_has_loaded(driver)
        element = driver.find_elements_by_css_selector(".a-pagination li a")[page_number - 1]
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        print("\n  Go to page {} ".format(page_number))
        self.page_has_loaded(driver)

    @allure.step('Select quantity')
    def select_quantity(self, driver, quantity_number):
        if len(driver.find_elements_by_css_selector("#selectQuantity > span > div > div > span")) > 0:
            driver.find_element_by_css_selector("#selectQuantity > span > div > div > span").click()
        else:
            print("There is no quantity dropdown")
            raise Exception("There is no quantity dropdown")
        driver.find_element_by_id("quantity_{}".format(quantity_number - 1)).click()
        print("\n  Selecting quantity {} from the search dropdown.".format(quantity_number))
        self.page_has_loaded(driver)

    @allure.step('Select a BRAND')
    def select_brand(self, driver, brands):
        for brand in brands:
            self.page_has_loaded(driver)
            element = driver.find_element_by_xpath("//li[contains(@id,'{}')]/span/a/div/label".format(brand))
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.find_element_by_xpath("//li[contains(@id,'{}')]/span/a/div/label".format(brand)).click()
            print("\n  Select {} from BRANDS".format(brand))

    @allure.step('Filtration of the price')
    def filter_the_price(self, driver, min_amount, max_amount):
        low_price = driver.find_element_by_id("low-price")
        low_price.clear()
        low_price.send_keys(min_amount)
        high_price = driver.find_element_by_id("high-price")
        high_price.clear()
        high_price.send_keys(max_amount)
        go_button_filtration = driver.find_element_by_xpath(
            "//*[@id='a-autoid-1-announce']/preceding-sibling::input[@type='submit']")
        go_button_filtration.click()

    def page_has_loaded(self, driver):
        print("\n  Checking if {} page is loaded.".format(driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        if page_state != 'complete':
            time.sleep(5)
