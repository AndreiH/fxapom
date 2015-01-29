#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import re

import pytest
from unittestzero import Assert

from fxapom.fxapom import FxATestAccount


@pytest.mark.nondestructive
@pytest.mark.skip_selenium
class TestCreateAccount(object):

    def test_create_new_account(self):
        acct = FxATestAccount(use_prod=False).create_account()
        Assert.true(acct.is_verified)

    def test_new_account_pw_does_not_contain_numbers(self):
        acct = FxATestAccount(use_prod=False).create_account()
        test_regex = re.compile('\d')
        Assert.equal(None, test_regex.search(acct.password))
