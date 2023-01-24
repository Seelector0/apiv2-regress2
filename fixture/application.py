from utils.api.delivery_serviches.delivery_services import ApiDeliveryServices
from utils.api.orders.orders import ApiOrder
from utils.api.parcels.parcels import ApiParcel
from utils.api.warehouses.warehouses import ApiWarehouse
from utils.http_methods import HttpMethods
from utils.api.shops.shops import ApiShop
from pathlib import Path
import requests


class Application:

    def __init__(self, base_url=None, response=None):
        self.download_directory = str(Path(Path.home(), "PycharmProjects", "Apiv2-regress-version2", "file"))
        self.logs_directory = str(Path(Path.home(), "PycharmProjects", "Apiv2-regress-version2", "logs"))
        self.base_url = base_url
        self.session = requests.Session()
        self.response = response
        self.http_method = HttpMethods(self)
        self.shop = ApiShop(self)
        self.warehouse = ApiWarehouse(self)
        self.service = ApiDeliveryServices(self)
        self.order = ApiOrder(self)
        self.parcel = ApiParcel(self)

    def open_session(self, data, headers):
        self.response = self.session.post(url=self.base_url, data=data, headers=headers)
        return self.response

    def download_file(self, name: str, value_id: str, expansion: str,  response):
        with open(file=f"{self.download_directory}/{name}-{value_id}.{expansion}", mode="wb") as label:
            return label.write(response.content)

    def close_session(self):
        self.session.close()
