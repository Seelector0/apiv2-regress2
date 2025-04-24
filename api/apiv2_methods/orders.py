from random import randrange
from utils.global_enums import INFO
from random import choice


class ApiOrder:

    def __init__(self, app):
        self.app = app
        self.link = "orders"
        self.method_xls = "application/vnd.ms-excel"
        self.method_xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    @staticmethod
    def calculate_declared_value(service, declared_value, delivery_sum, *prices):
        """Вычисление объявленной стоимости или возвращение переданной в тесте."""
        if service == "FivePost":
            return sum(prices)
        return declared_value if declared_value is not None else (delivery_sum + sum(prices))

    def generate_barcodes_and_shop_numbers(self, service, barcode_1, barcode_2, shop_number_1, shop_number_2):
        """Генерация или использование переданных штрих-кодов и номеров магазинов."""
        if service != "Boxberry":
            shop_number_1 = shop_number_1 or self.app.dicts.generate_random_number()
            shop_number_2 = shop_number_2 or self.app.dicts.generate_random_number()
            barcode_1 = barcode_1 or self.app.dicts.generate_random_number()
            barcode_2 = barcode_2 or self.app.dicts.generate_random_number()
        return shop_number_1, shop_number_2, barcode_1, barcode_2

    def generate_calculate_dimensions(self, dimension_1=None, dimension_2=None, total_dimensions=None):
        """Вычисляет два размера и их сумму. Если размеры не переданы, генерирует их."""
        dimension_1 = dimension_1 or self.app.dicts.dimension()
        dimension_2 = dimension_2 or self.app.dicts.dimension()
        total_dimensions = total_dimensions or {
            'length': max(dimension_1['length'], dimension_2['length']),
            'width': max(dimension_1['width'], dimension_2['width']),
            'height': dimension_1['height'] + dimension_2['height']
        }
        return dimension_1, dimension_2, total_dimensions

    def post_single_order(self, shop_id, warehouse_id, payment_type: str, delivery_type: str, service: str,
                          shop_barcode: str = None, declared_value: float = None, delivery_sum: float = 100.24,
                          cod: float = None, weight: float = 3, tariff: str = None, delivery_point_code: str = None,
                          data: str = None, delivery_time: dict = None, email: str = "test@mail.ru",
                          company_name: str = None, comment: str = "Тестовый комментарий", country_code: str = None,
                          price_1: float = 1000, price_2: float = 1000, price_3: float = 1000,
                          items_declared_value: int = 1000, pickup_time_period: str = None, date_pickup: str = None,
                          type_order: str = None, intake_point_code: str = None):
        r"""Метод создания одноместного заказа.
        :param shop_id: Id магазина.
        :param shop_barcode: Штрих код заказа.
        :param warehouse_id: Id склада.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param delivery_sum: Стоимость доставки.
        :param cod: Наложенный платеж, руб.
        :param weight: Общий все заказа.
        :param delivery_type: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param tariff: Тариф создания заказа.
        :param delivery_point_code: Идентификатор точки доставки.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param country_code: Код страны назначения.
        :param email: Электронная почта получателя.
        :param company_name:  Наименование компании для возвратных заказов.
        :param comment: Комментарий к заказу.
        :param price_1: Цена первой товарной позиции.
        :param price_2: Цена второй товарной позиции.
        :param price_3: Цена третий товарной позиции.
        :param items_declared_value: Цена товарной позиции.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        :param type_order: Тип заказа.
        :param intake_point_code: Идентификатор точки сдачи возврата.
        """
        declared_value_result = self.calculate_declared_value(service, declared_value, delivery_sum,
                                                              price_1, price_2, price_3)
        single_order = self.app.dicts.form_order(shop_id=shop_id, warehouse_id=warehouse_id, shop_barcode=shop_barcode,
                                                 payment_type=payment_type, declared_value=declared_value_result,
                                                 delivery_sum=delivery_sum, cod=cod,
                                                 dimension=self.app.dicts.dimension(), weight=weight,
                                                 delivery_type=delivery_type, service=service,
                                                 tariff=tariff, data=data, delivery_time=delivery_time,
                                                 delivery_point_code=delivery_point_code, company_name=company_name,
                                                 comment=comment, email=email, country_code=country_code,
                                                 pickup_time_period=pickup_time_period, date_pickup=date_pickup,
                                                 type_order=type_order, intake_point_code=intake_point_code)
        single_order["places"] = self.app.dicts.places(places=[
            self.app.dicts.items(name="Стол", price=price_1, count=1, weight=1, vat="5",
                                 items_declared_value=items_declared_value),
            self.app.dicts.items(name="Стул", price=price_2, count=1, weight=1, vat="7",
                                 items_declared_value=items_declared_value),
            self.app.dicts.items(name="Пуфик", price=price_3, count=1, weight=1, vat="10",
                                 items_declared_value=items_declared_value)
        ])
        result = self.app.http_method.post(link=self.link, json=single_order)
        return self.app.http_method.return_result(response=result)

    def post_single_order_minimal(self, shop_id, warehouse_id, payment_type: str, delivery_type: str, service: str,
                                  shop_barcode: str = None, declared_value: float = None, delivery_sum: float = 100.24,
                                  cod: float = None, weight: float = 3, tariff: str = None,
                                  delivery_point_code: str = None,
                                  data: str = None, delivery_time: dict = None, country_code: str = None,
                                  price_1: float = 1000,
                                  price_2: float = 1000, price_3: float = 1000, items_declared_value: int = 1000,
                                  pickup_time_period: str = None, date_pickup: str = None, type_order: str = None,
                                  intake_point_code: str = None):
        r"""Метод создания одноместного заказа с минимальным набором атрибутов.
        :param shop_id: Id магазина.
        :param shop_barcode: Штрих код заказа.
        :param warehouse_id: Id склада.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param delivery_sum: Стоимость доставки.
        :param cod: Наложенный платеж, руб.
        :param weight: Общий все заказа.
        :param delivery_type: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param tariff: Тариф создания заказа.
        :param delivery_point_code: Идентификатор точки доставки.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param country_code: Код страны назначения.
        :param price_1: Цена первой товарной позиции.
        :param price_2: Цена второй товарной позиции.
        :param price_3: Цена третий товарной позиции.
        :param items_declared_value: Цена товарной позиции.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        :param type_order: Тип заказа.
        :param intake_point_code: Идентификатор точки сдачи возврата.
        """
        dimension = None
        declared_value_result = self.calculate_declared_value(service, declared_value, delivery_sum,
                                                              price_1, price_2, price_3)
        if service != "RussianPost":
            dimension = self.app.dicts.dimension()
        single_order = self.app.dicts.form_order(shop_id=shop_id, warehouse_id=warehouse_id, shop_barcode=shop_barcode,
                                                 payment_type=payment_type, declared_value=declared_value_result,
                                                 delivery_sum=delivery_sum, cod=cod,
                                                 dimension=dimension, weight=weight,
                                                 delivery_type=delivery_type, service=service,
                                                 tariff=tariff, data=data, delivery_time=delivery_time,
                                                 delivery_point_code=delivery_point_code, country_code=country_code,
                                                 pickup_time_period=pickup_time_period, date_pickup=date_pickup,
                                                 type_order=type_order, intake_point_code=intake_point_code)
        if service != "RussianPost":
            single_order["places"] = self.app.dicts.places(places=[
                self.app.dicts.items(name="Стол", price=price_1, count=1, weight=1, vat="10",
                                     items_declared_value=items_declared_value),
                self.app.dicts.items(name="Стул", price=price_2, count=1, weight=1, vat="10",
                                     items_declared_value=items_declared_value),
                self.app.dicts.items(name="Пуфик", price=price_3, count=1, weight=1, vat="10",
                                     items_declared_value=items_declared_value)
            ])
        result = self.app.http_method.post(link=self.link, json=single_order)
        return self.app.http_method.return_result(response=result)

    def post_multi_order(self, shop_id, warehouse_id, payment_type: str, delivery_type: str,
                         service: str, declared_value: float = None, delivery_sum: float = 100.24, cod: float = None,
                         weight: float = 3, total_dimension: dict = None, tariff: str = None,
                         delivery_point_code: str = None, data: str = None, delivery_time: dict = None,
                         email: str = "test@mail.ru", comment: str = "Тестовый комментарий", price_1: float = 1000,
                         weight_1: float = 1, barcode_1: str = None, shop_number_1: str = None,
                         dimension_1: dict = None, price_2: float = 1000, weight_2: float = 2, barcode_2: str = None,
                         shop_number_2: str = None, dimension_2: dict = None, pickup_time_period: str = None,
                         date_pickup: str = None):
        r"""Метод создания многоместного заказа.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param payment_type: Тип оплаты 'Paid' - Полная предоплата, 'PayOnDelivery' - Оплата при получении.
        :param declared_value: Объявленная стоимость.
        :param delivery_sum: Стоимость доставки.
        :param cod: Наложенный платеж, руб.
        :param weight: Общий все заказа.
        :param total_dimension: Габариты заказа.
        :param delivery_type: Тип доставки 'Courier', 'DeliveryPoint', 'PostOffice'.
        :param service: Код СД.
        :param tariff: Тариф создания заказа.
        :param delivery_point_code: Идентификатор точки доставки.
        :param data: Дата доставки.
        :param delivery_time: Если указанна поле 'data', то delivery_time обязателен для курьерского заказа
        :param email: Электронная почта получателя.
        :param comment: Комментарий к заказу.
        :param price_1: Цена первого грузоместа.
        :param weight_1: Вес первого грузоместа.
        :param barcode_1: Штрих-код первого грузоместа.
        :param shop_number_1: Номер в магазине первого грузоместа.
        :param dimension_1: Габариты грузоместа.
        :param price_2: Цена первого грузо места.
        :param weight_2: Вес первого грузо места.
        :param barcode_2: Штрих-код первого грузоместа.
        :param shop_number_2: Номер в магазине первого грузоместа.
        :param dimension_2: Габариты грузоместа.
        :param pickup_time_period: Дата привоза на склад.
        :param date_pickup: Временной интервал.
        """
        declared_value_result = self.calculate_declared_value(service, declared_value, delivery_sum,
                                                              price_1, price_2)
        shop_number_1, shop_number_2, barcode_1, barcode_2, = (self.generate_barcodes_and_shop_numbers(service,
                                                                                                       shop_number_1,
                                                                                                       shop_number_2,
                                                                                                       barcode_1,
                                                                                                       barcode_2))
        dimension_1, dimension_2, total_dimension = self.generate_calculate_dimensions(dimension_1, dimension_2,
                                                                                       total_dimension)
        multi_order = self.app.dicts.form_order(shop_id=shop_id, warehouse_id=warehouse_id, payment_type=payment_type,
                                                declared_value=declared_value_result,
                                                delivery_sum=delivery_sum, cod=cod,
                                                dimension=total_dimension, weight=weight,
                                                delivery_type=delivery_type, service=service, tariff=tariff, data=data,
                                                delivery_time=delivery_time, delivery_point_code=delivery_point_code,
                                                comment=comment, email=email, date_pickup=date_pickup,
                                                pickup_time_period=pickup_time_period)
        multi_order["places"] = [
            self.app.dicts.form_cargo_items(items=self.app.dicts.items(name="Стол", price=price_1, count=1,
                                                                       weight=weight_1, vat="10"),
                                            barcode=barcode_1, shop_number=shop_number_1,
                                            dimension=dimension_1, weight=1),
            self.app.dicts.form_cargo_items(items=self.app.dicts.items(name="Стул", price=price_2, count=1,
                                                                       weight=weight_2, vat="10"),
                                            barcode=barcode_2, shop_number=shop_number_2,
                                            dimension=dimension_2, weight=2)
        ]
        result = self.app.http_method.post(link=self.link, json=multi_order)
        return self.app.http_method.return_result(response=result)

    @staticmethod
    def open_file(folder: str, file: str, method: str):
        r"""Метод отправки файла.
        :param folder: Название папки.
        :param file: Имя файла.
        :param method: Метод отправки файла.
        """
        return [("file", (f"{file}", open(file=f"utils/folder_with_orders/{folder}/{file}", mode="rb"), method))]

    def post_import_order_format_metaship(self, shop_id, warehouse_id, code: str, file_extension: str):
        r"""Метод создания заказа из файла XLSX или XLS формата Metaship.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param code: Код СД.
        :param file_extension: Exel файл с расширением xlsx или xls.
        """
        orders = f"orders_{code}.{file_extension}"
        body = self.app.dicts.form_order_from_file(shop_id=shop_id, warehouse_id=warehouse_id)
        if file_extension == "xls":
            file = self.open_file(folder="format_metaship", file=orders, method=self.method_xls)
        elif file_extension == "xlsx":
            file = self.open_file(folder="format_metaship", file=orders, method=self.method_xlsx)
        else:
            return f"Файл {file_extension} не поддерживается"
        result = self.app.http_method.post(link=f"import/{self.link}", data=body, files=file)
        return self.app.http_method.return_result(response=result)

    def post_import_order_format_russian_post(self, shop_id, warehouse_id, file_extension: str):
        r"""Метод создания заказа из файла XLSX или XLS формата СД RussianPost.
        :param shop_id: Id магазина.
        :param warehouse_id: Id склада.
        :param file_extension: Exel файл с расширением xlsx или xls.
        """
        orders = f"orders_format_russian_post.{file_extension}"
        body = self.app.dicts.form_order_from_file(shop_id=shop_id, warehouse_id=warehouse_id, type_="russian_post")
        if file_extension == "xls":
            file = self.open_file(folder="format_russian_post", file=orders, method=self.method_xls)
        elif file_extension == "xlsx":
            file = self.open_file(folder="format_russian_post", file=orders, method=self.method_xlsx)
        else:
            return f"Файл {file_extension} не поддерживается"
        result = self.app.http_method.post(link=f"import/{self.link}", data=body, files=file)
        return self.app.http_method.return_result(response=result)

    def get_order_search(self, query: str):
        r"""Метод поиска по заказам.
        :param query: Поле поиска по ID, shop_number и тд.
        """
        params = dict(query=query)
        result = self.app.http_method.get(link=f"{self.link}/search", params=params)
        return self.app.http_method.return_result(response=result)

    def get_orders(self):
        """Метод возвращает список заказов."""
        result = self.app.http_method.get(link=self.link, params={'limit': 10})
        return self.app.http_method.return_result(response=result)

    def get_order_id(self, order_id: str):
        r"""Метод получения информации о заказе по его id.
        :param order_id: Идентификатор заказа.
        """
        result = self.app.http_method.get(link=f"{self.link}/{order_id}")
        return self.app.http_method.return_result(response=result)

    def put_order(self, order_id: str, weight: str, length: str, width: str, height: str, family_name: str,
                  delivery_service: str = None, first_name: str = None, second_name: str = None,
                  phone_number: str = None, email: str = None, address: str = None, comment: str = None):
        r"""Метод обновления заказа для СД RussianPost, LPost и Dalli.
        :param order_id: Идентификатор заказа.
        :param weight: Общий вес заказа.
        :param length: Длинна.
        :param width: Ширина.
        :param height: Высота.
        :param family_name: Фамилия получателя.
        :param first_name: Имя получателя.
        :param second_name: Отчество получателя.
        :param phone_number: Телефон получателя.
        :param email: Email получателя.
        :param delivery_service: СД.
        :param address: Адрес получателя.
        :param comment: Комментарий к заказу.
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
        put_order = result_get_order_by_id.json()["data"]["request"]
        put_order["weight"] = weight
        put_order["dimension"]["length"] = length
        put_order["dimension"]["width"] = width
        put_order["dimension"]["height"] = height
        put_order["recipient"]["familyName"] = family_name
        put_order["recipient"]["firstName"] = first_name
        put_order["recipient"]["secondName"] = second_name
        put_order["recipient"]["phoneNumber"] = phone_number
        put_order["recipient"]["email"] = email
        put_order["recipient"]["address"] = dict(raw=address)
        put_order["comment"] = comment
        if delivery_service == "RussianPost":
            put_order["places"] = self.app.dicts.places(places=[
                self.app.dicts.items(name="Книга", price=1000, count=1, weight=3, vat="10"),
                self.app.dicts.items(name="Шкаф", price=1000, count=1, weight=1, vat="10")
            ])
        result = self.app.http_method.put(link=f"{self.link}/{order_id}", json=put_order)
        return self.app.http_method.return_result(response=result)

    def patch_order_weight(self, order_id: str, weight: int):
        r"""Метод редактирования веса в заказе для СД Boxberry, Cdek, Dpd, FivePost, RussianPost.
        :param order_id: Идентификатор заказа.
        :param weight: Новый вес заказа.
        """
        patch_weight = self.app.dicts.form_patch_body(op="replace", path="weight", value=weight)
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_weight)
        return self.app.http_method.return_result(response=result)

    def patch_order_recipient(self, order_id: str, phone_number: str, email: str, family_name: str = None,
                              first_name: str = None, second_name: str = None, address: dict = None):
        r"""Метод редактирования данных о получателе для СД FivePost и Cdek.
        :param order_id: Идентификатор заказа.
        :param family_name: Фамилия получателя.
        :param first_name: Имя получателя.
        :param second_name: Отчество получателя.
        :param phone_number: Новый телефонный номер получателя.
        :param email: Новый email получателя.
        :param address: Адрес получателя.
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
        recipient_order = result_get_order_by_id.json()["data"]["request"]["recipient"]
        if family_name is None:
            family_name = recipient_order["familyName"]
        if first_name is None:
            first_name = recipient_order["firstName"]
        if second_name is None:
            second_name = recipient_order["secondName"]
        if address is None:
            address = recipient_order["address"]
        patch_order = self.app.dicts.form_patch_body(op="replace", path="recipient",
                                                     value=self.app.dicts.recipient(address=address, email=email,
                                                                                    family_name=family_name,
                                                                                    first_name=first_name,
                                                                                    second_name=second_name,
                                                                                    phone_number=phone_number))
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_order)
        return self.app.http_method.return_result(response=result)

    def patch_order_items_five_post(self, order_id: str, items_name: str):
        r"""Метод редактирования заказа для СД FivPost.
        Все созданные места стираются и заменяются новыми.
        :param order_id: Идентификатор заказа.
        :param items_name: Название товара.
        """

        patch_items = self.app.dicts.form_patch_body(op="replace", path="places",
                                                     value=self.app.dicts.places(places=[self.app.dicts.items(
                                                         name=items_name, price=500, count=2, weight=1,
                                                         vat=choice(INFO.five_post_vats)["code"])]))
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_items)
        return self.app.http_method.return_result(response=result)

    def patch_order_items_cdek(self, order_id: str, name_1: str, name_2: str):
        r"""Метод редактирования заказа для СД Cdek.
        Все созданные места стираются и заменяются новыми.
        :param order_id: Идентификатор заказа.
        :param name_1: Название первого товара.
        :param name_2: Название второго товара.
        """
        patch_order = self.app.dicts.form_patch_body(op="replace", path="places", value=[
            self.app.dicts.replace_items_cdek(name=name_1), self.app.dicts.replace_items_cdek(name=name_2)
        ])
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_order)
        return self.app.http_method.return_result(response=result)

    def patch_delivery_courier_cdek(self, order_id: str, time_from: str, time_to: str):
        r"""Метод редактирование интервалов доставки для СД Cdek.
        :param order_id: Идентификатор заказа
        :param time_from: Время с кого часа ожидания.
        :param time_to: Время по какой час ожидания.
        :return:
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
        tariff = result_get_order_by_id.json()["data"]["request"]["delivery"]["tariff"]
        patch_order = self.app.dicts.form_patch_body(op="replace", path="delivery",
                                                     value=self.app.dicts.delivery_interval(tariff=tariff,
                                                                                            time_from=time_from,
                                                                                            time_to=time_to))
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_order)
        return self.app.http_method.return_result(response=result)

    def patch_order(self, order_id: str, name: str, price: float, count: int, weight: float, barcode: str = None):
        r"""Метод редактирования поля в заказе для СД Cdek и Dpd.
        :param order_id: Идентификатор заказа.
        :param name: Наименование товарной позиции.
        :param price: Цена товарной позиции.
        :param count: Количество штук.
        :param weight: Вес товарной позиции.
        :param barcode: Штрих код товарной позиции
        """
        patch_order = self.app.dicts.form_patch_body(op="replace", path="places", value=[
            self.app.dicts.form_cargo_items(items=self.app.dicts.items(name=name, price=price, count=count,
                                                                       weight=weight, vat="0"), barcode=barcode)
        ])
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_order)
        return self.app.http_method.return_result(response=result)

    def patch_order_add_item(self, order_id: str):
        r"""Метод добавление места в заказ СД Cdek, Dpd, DostavkaClub.
        Для СД DPD старые места удаляются и добавляются новые
        :param order_id: Идентификатор заказа.
        """
        result_get_order_by_id = self.get_order_id(order_id=order_id)
        items = result_get_order_by_id.json()["data"]["request"]["places"]
        patch_order = self.app.dicts.form_patch_body(op="replace", path="places", value=[
            *items,
            self.app.dicts.form_cargo_items(items=self.app.dicts.items(name="Пуфик", price=1000, count=1, vat="10"),
                                            barcode=f"{randrange(1000000, 9999999)}", weight=4)
        ])
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_order)
        return result_get_order_by_id, self.app.http_method.return_result(response=result)

    def patch_create_multy_order(self, order_id: str, items: list):
        r"""Создание многоместного из одноместного заказа для СД TopDelivery.
        :param order_id: Идентификатор заказа.
        :param items: Список товаров из заказа.
        """
        list_items = []
        for i in items:
            list_items.append(self.app.dicts.form_cargo_items(items=i, dimension=self.app.dicts.dimension(),
                                                              shop_number=f"{randrange(1000000, 9999999)}"))
        path_order = self.app.dicts.form_patch_body(op="replace", path="places", value=list_items)
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=path_order)
        return self.app.http_method.return_result(response=result)

    def patch_order_cancelled(self, order_id: str, headers: dict = None):
        r"""Метод отмены заказа.
        :param order_id: Идентификатор заказа.
        :param headers: Пользовательские заголовки.
        """
        patch_cancelled = self.app.dicts.form_patch_body(op="replace", path="state", value="cancelled")
        result = self.app.http_method.patch(link=f"{self.link}/{order_id}", json=patch_cancelled, headers=headers)
        return self.app.http_method.return_result(response=result)

    def delete_order(self, order_id: str):
        r"""Метод удаления заказа.
        :param order_id: Идентификатор заказа.
        """
        return self.app.http_method.delete(link=f"{self.link}/{order_id}")

    def get_order_patches(self, order_id: str):
        r"""Метод получение PATCH изменений по заказу.
        :param order_id: Идентификатор заказа.
        """
        result = self.app.http_method.get(link=f"{self.link}/{order_id}/patches")
        return self.app.http_method.return_result(response=result)

    def get_order_statuses(self, order_id: str):
        r"""Метод получение информации об истории изменения статусов заказа.
        :param order_id: Идентификатор заказа.
        """
        result = self.app.http_method.get(link=f"{self.link}/{order_id}/statuses")
        return self.app.http_method.return_result(response=result)

    def get_order_details(self, order_id: str):
        r"""Метод получение подробной информации о заказе.
        :param order_id: Идентификатор заказа.
        """
        result = self.app.http_method.get(link=f"{self.link}/{order_id}/details")
        return self.app.http_method.return_result(response=result)

    def get_generate_security_code(self, order_id):
        r"""Получение кода выдачи заказа.
        :param order_id: Идентификатор заказа.
        """
        result = self.app.http_method.get(link=f"{self.link}/{order_id}/generate_security_code")
        return self.app.http_method.return_result(response=result)
