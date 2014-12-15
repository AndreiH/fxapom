#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from fxapom.fxapom import FxATestAccount
from fxapom.fxapom import WebDriverFxA


@pytest.mark.nondestructive
class TestLogin(object):

    _fxa_logged_in_indicator_locator = (By.ID, 'loggedin')

    @pytest.mark.credentials
    def test_existing_user_can_sign_in(self, mozwebqa):
        fxa = WebDriverFxA(mozwebqa)
        user = mozwebqa.credentials.get('default')
        fxa.sign_in(user['email'], user['password'])
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._fxa_logged_in_indicator_locator).is_displayed())

    def test_newly_created_user_can_sign_in(self, mozwebqa):
        acct = FxATestAccount(use_prod=False).create_account()
        fxa = WebDriverFxA(mozwebqa)
        fxa.sign_in(acct.email, acct.password)
        WebDriverWait(mozwebqa.selenium, mozwebqa.timeout).until(
            lambda s: s.find_element(*self._fxa_logged_in_indicator_locator).is_displayed())
