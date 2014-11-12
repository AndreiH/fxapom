#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class Base(object):

    def __init__(self, selenium, timeout=60, default_implicit_wait=10):
        self.selenium = selenium
        self.timeout = timeout
        self.default_implicit_wait = default_implicit_wait
        self._main_window_handle = self.selenium.current_window_handle
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    def switch_to_main_window(self):
        self.selenium.switch_to_window(self._main_window_handle)

    def is_element_present(self, *locator):
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_visible(self, *locator):
        count = 0
        while not self.is_element_visible(*locator):
            time.sleep(1)
            count += 1
            if count == self.timeout:
                raise Exception(':'.join(locator) + " is not visible")

    def is_element_visible(self, *locator):
        try:
            return self._selenium_root.find_element(*locator).is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False

    def close_window(self):
        self.selenium.close()
