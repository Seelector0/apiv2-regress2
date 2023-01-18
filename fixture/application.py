import requests


class Application:

    def __init__(self):
        self.session = requests.Session()

    def open_session(self, url, data, headers):
         response = self.session.post(url=url, data=data, headers=headers)
         return response

    def session_close(self):
        self.session.close()

