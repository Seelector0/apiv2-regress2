from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


class SettingsDeliveryServices:

    def __init__(self, app):
        self.app = app

    def russian_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки RussianPost к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        russian_post = self.app.dicts.form_connection_type(delivery_service_code="RussianPost")
        russian_post["data"]["token"] = os.getenv("RP_TOKEN")
        russian_post["data"]["secret"] = os.getenv("RP_SECRET")
        if aggregation:
            russian_post = self.app.dicts.form_connection_type(delivery_service_code="RussianPost", aggregation=True)
        russian_post["data"]["intakePostOfficeCode"] = "101000"
        return russian_post

    def topdelivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки TopDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        topdelivery = self.app.dicts.form_connection_type(delivery_service_code="TopDelivery")
        topdelivery["data"]["username"] = os.getenv("TD_USER_NAME")
        topdelivery["data"]["password"] = os.getenv("TD_PASSWORD")
        topdelivery["data"]["basicLogin"] = os.getenv("TD_BASIC_LOGIN")
        topdelivery["data"]["basicPassword"] = os.getenv("TD_BASIC_PASSWORD")
        if aggregation:
            topdelivery = self.app.dicts.form_connection_type(delivery_service_code="TopDelivery", aggregation=True)
        return topdelivery

    def boxberry(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Boxberry к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        boxberry = self.app.dicts.form_connection_type(delivery_service_code="Boxberry")
        boxberry["data"]["token"] = os.getenv("BB_API_TOKEN")
        if aggregation:
            boxberry = self.app.dicts.form_connection_type(delivery_service_code="Boxberry", aggregation=True)
        boxberry["data"]["intakeDeliveryPointCode"] = os.getenv("BB_INTAKE_DELIVERY_POINT_CODE")
        return boxberry

    def cdek(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cdek к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        cdek = self.app.dicts.form_connection_type(delivery_service_code="Cdek")
        cdek["data"]["account"] = os.getenv("CDEK_ACCOUNT")
        cdek["data"]["password"] = os.getenv("CDEK_PASSWORD")
        if aggregation:
            cdek = self.app.dicts.form_connection_type(delivery_service_code="Cdek", aggregation=True)
        cdek["data"]["shipmentPointCode"] = "AKHT1"
        return cdek

    def dpd(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dpd к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        dpd = self.app.dicts.form_connection_type(delivery_service_code="Dpd")
        dpd["data"]["clientNumber"] = os.getenv("DPD_CLIENT_NUMBER")
        dpd["data"]["clientKey"] = os.getenv("DPD_CLIENT_KEY")
        if aggregation:
            dpd = self.app.dicts.form_connection_type(delivery_service_code="Dpd", aggregation=True)
        dpd["data"]["intakePointCode"] = "M16"
        return dpd

    def cse(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Cse к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        cse = self.app.dicts.form_connection_type(delivery_service_code="Cse")
        cse["data"]["login"] = os.getenv("CSE_LOGIN")
        cse["data"]["password"] = os.getenv("CSE_PASSWORD")
        cse["data"]["token"] = os.getenv("CSE_TOKEN")
        if aggregation:
            cse = self.app.dicts.form_connection_type(delivery_service_code="Cse", aggregation=True)
        return cse

    def five_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки FivePost к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        five_post = self.app.dicts.form_connection_type(delivery_service_code="FivePost")
        five_post["data"]["apiKey"] = os.getenv("FIVE_POST_API_KEY")
        five_post["data"]["partnerNumber"] = os.getenv("FIVE_POST_PARTNER_NUMBER")
        five_post["data"]["baseWeight"] = int(os.getenv("FIVE_POST_BASE_WEIGHT"))
        if aggregation:
            five_post = self.app.dicts.form_connection_type(delivery_service_code="FivePost", aggregation=True)
        return five_post

    def yandex_go(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexGo к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        yandex_go = self.app.dicts.form_connection_type(delivery_service_code="YandexGo")
        yandex_go["data"]["token"] = os.getenv("YA_GO_TOKEN")
        if aggregation:
            yandex_go = self.app.dicts.form_connection_type(delivery_service_code="YandexGo", aggregation=True)
        return yandex_go

    def yandex_delivery(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки YandexDelivery к магазину.
        :param aggregation: Тип подключения СД по агрегации."""
        yandex_delivery = self.app.dicts.form_connection_type(delivery_service_code="YandexDelivery")
        yandex_delivery["data"]["token"] = os.getenv("YA_DELIVERY_TOKEN")
        yandex_delivery["data"]["inn"] = os.getenv("YA_DELIVERY_INN")
        yandex_delivery["data"]["intakePointCode"] = os.getenv("YA_DELIVERY_INTAKE_POINT_CODE")
        if aggregation:
            yandex_delivery = self.app.dicts.form_connection_type(delivery_service_code="YandexDelivery",
                                                                  aggregation=True)
        return yandex_delivery

    def dostavka_club(self):
        """Настройки подключения службы доставки DostavkaClub к магазину."""
        dostavka_club = self.app.dicts.form_connection_type(delivery_service_code="DostavkaClub")
        dostavka_club["data"]["login"] = os.getenv("CLUB_LOGIN")
        dostavka_club["data"]["pass"] = os.getenv("CLUB_PASSWORD")
        return dostavka_club

    def dostavka_guru(self):
        """Настройки подключения службы доставки DostavkaGuru к магазину."""
        dostavka_guru = self.app.dicts.form_connection_type(delivery_service_code="DostavkaGuru")
        dostavka_guru["data"]["partnerId"] = int(os.getenv("GURU_PARTNER_ID"))
        dostavka_guru["data"]["key"] = os.getenv("GURU_KEY")
        return dostavka_guru

    def l_post(self):
        """Настройки подключения службы доставки LPost к магазину по интеграции."""
        l_post = self.app.dicts.form_connection_type(delivery_service_code="LPost")
        l_post["data"]["secret"] = os.getenv("L_POST_SECRET")
        return l_post

    def dalli(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Dalli к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        dalli = self.app.dicts.form_connection_type(delivery_service_code="Dalli")
        dalli["data"]["token"] = os.getenv("DALLI_TOKEN")
        if aggregation:
            dalli = self.app.dicts.form_connection_type(delivery_service_code="Dalli", aggregation=True)
        return dalli

    def halva(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Halva к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        halva = self.app.dicts.form_connection_type(delivery_service_code="Halva")
        halva["data"]["client"] = os.getenv("HALVA_CLIENT_AND_KEY")
        halva["data"]["key"] = os.getenv("HALVA_CLIENT_AND_KEY")
        if aggregation:
            halva = self.app.dicts.form_connection_type(delivery_service_code="Halva", aggregation=True)
        return halva

    def kaz_post(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки KazPost к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        kaz_post = self.app.dicts.form_connection_type(delivery_service_code="KazPost")
        kaz_post["data"]["key"] = os.getenv("KAZ_POST_KEY")
        kaz_post["data"]["intakePostOfficeCode"] = os.getenv("KAZ_POST_INTAKE_POST_OFFICE_CODE")
        kaz_post["data"]["bin"] = os.getenv("KAZ_POST_BIN")
        kaz_post["data"]["counterparty"] = os.getenv("KAZ_POST_COUNTERPARTY")
        kaz_post["data"]["acceptanceEmail"] = os.getenv("KAZ_POST_ACCEPTANCE_EMAIL")
        kaz_post["data"]["agreementDate"] = "2024-01-01"
        kaz_post["data"]["agreementNumber"] = "1234"
        if aggregation:
            kaz_post = self.app.dicts.form_connection_type(delivery_service_code="KazPost", aggregation=True)
        return kaz_post

    def alemtat(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки AlemTat к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        alemtat = self.app.dicts.form_connection_type(delivery_service_code="AlemTat")
        alemtat["data"]["apiKey"] = os.getenv("ALEMTAT_KEY")
        alemtat["data"]["card"] = os.getenv("ALEMTAT_CARD")
        alemtat["data"]["contract"] = os.getenv("ALEMTAT_CONTRACT")
        alemtat["data"]["receivingStation"] = os.getenv("ALEMTAT_RECEIVING_STATION")
        if aggregation:
            alemtat = self.app.dicts.form_connection_type(delivery_service_code="AlemTat", aggregation=True)
        return alemtat

    def pony_express(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки PonyExpress к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        pony_express = self.app.dicts.form_connection_type(delivery_service_code="PonyExpress")
        pony_express["data"]["accessKey"] = os.getenv("PONY_ACCESS_KEY")
        if aggregation:
            pony_express = self.app.dicts.form_connection_type(delivery_service_code="PonyExpress", aggregation=True)
        return pony_express

    def metaship(self):
        """Настройки подключения службы доставки MetaShip к магазину по агрегации."""
        metaship = self.app.dicts.form_connection_type(delivery_service_code="MetaShip", aggregation=True)
        return metaship

    def pecom(self, aggregation: bool = None):
        r"""Настройки подключения службы доставки Pecom к магазину.
        :param aggregation: Тип подключения СД по агрегации.
        """
        pecom = self.app.dicts.form_connection_type(delivery_service_code="Pecom")
        pecom["data"]["login"] = os.getenv("PECOM_LOGIN")
        pecom["data"]["apiKey"] = os.getenv("PECOM_API_KEY")
        pecom["data"]["senderWarehouseId"] = os.getenv("PECOM_SENDER_WAREHOUSE_ID")
        if aggregation:
            pecom = self.app.dicts.form_connection_type(delivery_service_code="Pecom", aggregation=True)
        return pecom
