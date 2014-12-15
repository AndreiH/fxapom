#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from base import Base

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


class SignIn(Base):

    _fox_logo_locator = (By.ID, 'fox-logo')
    _email_input_locator = (By.CSS_SELECTOR, '.input-row .email')
    _next_button_locator = (By.ID, 'email-button')
    _password_input_locator = (By.ID, 'password')
    _sign_in_locator = (By.ID, 'submit-btn')
    _notice_form_locator = (By.CSS_SELECTOR, '#notice-form button')
    _age_selection_locator = (By.ID, 'fxa-age-year')
    _email_verification_message_locator = (By.CSS_SELECTOR, '.verification-email-message')

    def __init__(self, testsetup):
        Base.__init__(self, testsetup)

        if len(self.selenium.window_handles) > 1:
            self.popup = True
            for handle in self.selenium.window_handles:
                self.selenium.switch_to.window(handle)
                if self.is_element_present(*self._fox_logo_locator):
                    self.wait_for_element_visible(*self._email_input_locator)
                    self._sign_in_window_handle = handle
                    break
            else:
                raise Exception('Popup has not loaded')
        else:
            self.popup = False

    @property
    def email(self):
        """Get the value of the email field."""
        return self.selenium.find_element(*self._email_locator).get_attribute('value')

    @email.setter
    def email(self, value):
        """Set the value of the email field."""
        email = self.selenium.find_element(*self._email_input_locator)
        email.clear()
        email.send_keys(value)

    @property
    def login_password(self):
        """Get the value of the login password field."""
        return self.selenium.find_element(*self._login_password_locator).get_attribute('value')

    @login_password.setter
    def login_password(self, value):
        """Set the value of the login password field."""
        password = self.selenium.find_element(*self._password_input_locator)
        password.clear()
        password.send_keys(value)

    def click_next(self, expect='password'):
        self.selenium.find_element(*self._next_button_locator).click()

    def click_sign_in(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        if self.popup:
            WebDriverWait(self.selenium, self.timeout).until(
                        lambda s: self._sign_in_window_handle not in self.selenium.window_handles)
            self.switch_to_main_window()

    def click_sign_up(self):
        self.selenium.find_element(*self._sign_in_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(
                    lambda s: self.is_element_visible(*self._email_verification_message_locator))
        self.switch_to_main_window()

    def edit_year_of_birth(self, option_value):
        element = self.selenium.find_element(*self._age_selection_locator)
        select = Select(element)
        select.select_by_value(option_value)

    def sign_in(self, email, password):
        """Signs in using the specified email address and password."""
        self.email = email
        if self.is_element_present(*self._next_button_locator):
            self.click_next(expect='password')
        self.login_password = password
        self.click_sign_in()

    def register(self, mozwebqa, email, password):
        """Registers using the specified email address and password."""
        # Not yet implemented for fxapom
        # self.email = email
        # self.login_password = password
        # self.edit_year_of_birth('1990')
        # self.click_sign_up()
        # verify_user = FxaTestUser()
        # verify_user.verify_new_user(mozwebqa)
