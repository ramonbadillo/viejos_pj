# -*- coding: utf-8 -*-
from lettuce import *
from lettuce_webdriver.util import AssertContextManager
from datetime import datetime

from selenium import webdriver


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()


@after.all
def close_browser(total):
    world.browser.quit()


def find_field_by_class(browser, attribute):
    xpath = "//input[@class='%s']" % attribute
    elems = browser.find_elements_by_xpath(xpath)
    return elems[0] if elems else False

@step('I go to "([^"]*)"')
def given_i_go_to_url(step, url):
    world.response = world.browser.get(url)


@step('I fill in field with id "([^"]*)" with "([^"]*)"')
def when_i_fill_in_field_with_id_group1_with_group2(step, field_id, value):
    with AssertContextManager(step):
        text_field = world.browser.find_element_by_id(field_id)
        text_field.clear()
        text_field.send_keys(value)
        
@step('I submit the form')
def and_i_submit_the_form(step):
    with AssertContextManager(step):
        form = world.browser.find_element_by_class_name('form-horizontal')
        form.submit()