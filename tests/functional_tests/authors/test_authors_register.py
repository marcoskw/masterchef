from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def test_open_authors_register(self):
        self.browser.get(self.live_server_url + '/authors/register')
