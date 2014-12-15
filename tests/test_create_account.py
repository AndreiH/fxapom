#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from unittestzero import Assert

from fxapom.fxapom import FxATestAccount


@pytest.mark.nondestructive
@pytest.mark.skip_selenium
class TestCreateAccount(object):

    def test_create_account(self):

        acct = FxATestAccount(use_prod=False).create_account()
        Assert.true(acct.is_verified)
