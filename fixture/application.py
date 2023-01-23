from utils.http_methods import HttpMethods
from utils.api.shops.shops import ApiShop
from pathlib import Path
import requests


class Application:

    def __init__(self, base_url=None, response=None):
        self.download_directory = str(Path(Path.home(), "PycharmProjects", "apiv2-regress-cabinet", "file"))
        self.base_url = base_url
        self.session = requests.Session()
        self.response = response
        self.http_method = HttpMethods(self)
        self.shop = ApiShop(self)

    def open_session(self, data, headers):
        self.response = self.session.post(url=self.base_url, data=data, headers=headers)
        return self.response

    def close_session(self):
        self.session.close()
