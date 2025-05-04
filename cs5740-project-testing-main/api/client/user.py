import aiohttp


class User:
    def __init__(self, username, password):
        self._auth = aiohttp.BasicAuth(username, password)
        self._username = username
        self._password = password

    def get_basic_auth(self) -> aiohttp.BasicAuth:
        return self._auth
