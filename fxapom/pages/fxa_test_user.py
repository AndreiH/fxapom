#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess

from user import MockUser


class FxaTestUser:
    """A base test class that can be extended by other tests to include utility methods."""

    email = 'webqa-%s@restmail.net' % \
            os.urandom(6).encode('hex')
    password = os.urandom(4).encode('hex')

    def generate_new_user(self):
        email = self.email
        password = self.password
        name=self.email.split('@')[0]
        return MockUser(email=self.email, password=self.password, name=self.email.split('@')[0])

    def create_user(self, mozwebqa):
        if '-dev.allizom' in mozwebqa.base_url:
            os.environ['PUBLIC_URL'] = 'https://stable.dev.lcip.org/auth/'
        else:
            os.environ['PUBLIC_URL'] = 'https://api.accounts.firefox.com/'
        self.email = 'webqa-%s@restmail.net' % \
                        os.urandom(6).encode('hex')
        self.password = os.urandom(4).encode('hex')

        # Create and verify the Firefox account
        subprocess.check_call(['fxa-client', '-e', self.email,
                                '-p', self.password, 'create'])
        subprocess.check_call(['fxa-client', '-e', self.email,
                                '-p', self.password, 'verify'])

        return MockUser(email=self.email, password=self.password, name=self.email.split('@')[0])

    def verify_new_user(self, mozwebqa):
        if '-dev.allizom' in mozwebqa.base_url:
            os.environ['PUBLIC_URL'] = 'https://stable.dev.lcip.org/auth/'
        else:
            os.environ['PUBLIC_URL'] = 'https://api.accounts.firefox.com/'

        subprocess.check_call(['fxa-client', '-e', self.email,
                                '-p', self.password, 'verify'])
