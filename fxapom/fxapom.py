#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import string
import random
from datetime import datetime

from fxa.core import Client
from fxa.tests.utils import TestEmailAccount


class WebDriverFxA(object):

    def __init__(self, testsetup):
        self.testsetup = testsetup

    def sign_in(self, email=None, password=None):
        """Signs in a user, either with the specified email address and password, or a returning user."""
        from pages.desktop.sign_in import SignIn
        sign_in = SignIn(self.testsetup)
        sign_in.sign_in(email, password)


class FxATestAccount:
    """A base test class that can be extended by other tests to include utility methods."""

    password = ''.join([random.choice(string.letters) for i in xrange(8)])

    def __init__(self, mozwebqa=None, use_prod=True):
        if mozwebqa and '-dev.allizom' in mozwebqa.base_url or (
            not use_prod):
            self.fxa_url = 'https://stable.dev.lcip.org/auth/'
        else:
            self.fxa_url = 'https://api.accounts.firefox.com/'

    def create_account(self):
        self.account = TestEmailAccount()
        client = Client(self.fxa_url)
        print 'fxapom created an account for email: %s at %s' % (self.account.email, datetime.now())
        # Create and verify the Firefox account
        self.session = client.create_account(self.account.email, self.password)
        m = self.account.wait_for_email(lambda m: "x-verify-code" in m["headers"])
        if not m:
            raise RuntimeError("Verification email was not received")
        self.session.verify_email_code(m["headers"]["x-verify-code"])
        return self

    @property
    def email(self):
        return self.account.email

    @property
    def is_verified(self):
        return self.session.get_email_status()['verified']
