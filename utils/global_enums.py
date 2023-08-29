

class OtherInfo:

    created_entity = ["id", "type", "url", "status"]

    entity_shops = ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"]

    entity_warehouse = ["id", "number", "name", "visibility", "address", "contact", "workingTime", "pickup",
                        "dpdPickupNum", "lPostWarehouseId", "yandexWarehouseId", "comment"]

    entity_order = ['id', 'number', 'addressTo', 'data', 'parcel', 'status', 'statusReason', 'state', 'stateMessage',
                    'created']

    entity_parcel = ['id', 'number', 'shop', 'deliveryServiceCode', 'data', 'created', 'deleted', 'state', 'stateTime']

    entity_intake = ['id', 'number', 'deliveryServiceId', 'status', 'createdAt', 'request']

    created_entity_widget = ['id', 'customerId', 'shopId', 'token', 'createdAt', 'updatedAt']

    entity_widget = ['id', 'customerId', 'shopId', 'token', 'script', 'createdAt', 'updatedAt']

    entity_moderation = ['id', 'connectionId', 'agreementId', 'customerAgreementId', 'credential', 'notified',
                         'expired']

    entity_webhook = ['id', 'shopId', 'url', 'name', 'secret', 'eventType', 'active', 'createdAt', 'updatedAt']

    entity_order_statuses = [
        {
            "name": "accepted",
            "title": "Заказ подтвержден",
            "description": "Заказ подтвержден интернет-магазином"
        },
        {
            "name": "arrived-to-city",
            "title": "Заказ прибыл в город получателя",
            "description": "Заказ прибыл в город получателя"
        },
        {
            "name": "arrived-to-city-warehouse",
            "title": "Прибыл в город получателя",
            "description": "Прямой поток. Заказ принят на складе службы в городе получателя"
        },
        {
            "name": "arrived-to-city-warehouse-after-delivery-failed",
            "title": "Не удачная попытка вручения",
            "description": "Прямой поток. Оформлен повторный приход на склад в городе-получателе. "
                           "Доставка не удалась по какой-либо причине, ожидается очередная попытка доставки. "
                           "Статус не означает возврат заказа отправителю"
        },
        {
            "name": "arrived-warehouse",
            "title": "Заказ поступил на склад службы",
            "description": "Заказ поступил на склад службы"
        },
        {
            "name": "cancelled",
            "title": "Отменен",
            "description": "Заказ отменен"
        },
        {
            "name": "cancelled-by-ds",
            "title": "Курьер отменил заказ",
            "description": "Курьер отменил заказ"
        },
        {
            "name": "courier-arrived",
            "title": "Курьер приехал в точку А",
            "description": "Курьер приехал в точку А"
        },
        {
            "name": "courier-found",
            "title": "Курьер найден и едет в точку А",
            "description": "Курьер найден и едет в точку А"
        },
        {
            "name": "courier-not-found",
            "title": "Не удалось найти курьера.",
            "description": "Не удалось найти курьера. Можно попробовать снова через некоторое время."
        },
        {
            "name": "created",
            "title": "Создан",
            "description": "Заказ подтвержден службой доставки"
        },
        {
            "name": "declined-by-client",
            "title": "Отказ клиента от выкупа заказа",
            "description": "Прямой поток. Клиент отказался от получения заказа. Заказ готовится к возврату отправителя"
        },
        {
            "name": "delivered",
            "title": "Доставлен",
            "description": "Получатель получил заказ через ПВЗ, постамат или курьером"
        },
        {
            "name": "delivery-point-client-cancelled",
            "title": "Клиент отказался от заказа",
            "description": "Клиент отказался от заказа"
        },
        {
            "name": "delivery-point-expired",
            "title": "Истёк срок хранения заказа",
            "description": "Истёк срок хранения заказа"
        },
        {
            "name": "dispatched-to-a-courier",
            "title": "Передан курьеру",
            "description": "Заказ передан курьеру на доставку"
        },
        {
            "name": "draft",
            "title": "Черновик",
            "description": "Заказ доступен для редактирования"
        },
        {
            "name": "error",
            "title": "Ошибка создания заказа",
            "description": "Заказ не прошел проверку в Metaship или в службе доставки"
        },
        {
            "name": "estimating",
            "title": "Процесс оценки",
            "description": "Идет процесс оценки заказа (подбор типа автомобиля по параметрам груза и расчет стоимости)"
        },
        {
            "name": "estimating-failed",
            "title": "Не удалось оценить заявку",
            "description": "Не удалось оценить заявку"
        },
        {
            "name": "expected-return",
            "title": "Готовится к возврату",
            "description": "Заказ находится в пути на полный возврат"
        },
        {
            "name": "expected-return-client-cancelled",
            "title": "Посылка уехала из ПВЗ по отказу клиента",
            "description": "Посылка уехала из ПВЗ по отказу клиента"
        },
        {
            "name": "expected-return-expired",
            "title": "Посылка уехала из ПВЗ по истечению срока хранения",
            "description": "Посылка уехала из ПВЗ по истечению срока хранения"
        },
        {
            "name": "intransit",
            "title": "Доставляется",
            "description": "Заказ доставляется"
        },
        {
            "name": "looking-for-courier",
            "title": "Идет поиск курьера",
            "description": "Идет поиск курьера"
        },
        {
            "name": "losted",
            "title": "Утерян",
            "description": "Заказ утерян при доставке"
        },
        {
            "name": "not-accepted-in-delivery-service",
            "title": "Не принят в СД",
            "description": "Заказ не принят в службе доставки"
        },
        {
            "name": "order-failed",
            "title": "При доставке заказа произошла ошибка",
            "description": "При доставке заказа произошла ошибка, дальнейшее выполнение невозможно"
        },
        {
            "name": "partially-delivered",
            "title": "Частично доставлен",
            "description": "Получатель получил часть заказа через ПВЗ, постамат или курьером"
        },
        {
            "name": "pending",
            "title": "Ждет подтверждения службы доставки",
            "description": "Заказ ожидает подтверждения от службы доставки"
        },
        {
            "name": "ready-for-approval",
            "title": "Успешно оценён",
            "description": "Заказ успешно оценён и ожидает подтверждения от интернет-магазина"
        },
        {
            "name": "return-arrived-warehouse",
            "title": "Возвращён на склад службы доставки",
            "description": "Заказ вернули на склад службы доставки"
        },
        {
            "name": "return-completed",
            "title": "Возвращён в магазин",
            "description": "Заказ вернули в интернет-магазин"
        },
        {
            "name": "return-partially-completed",
            "title": "Частичный возврат заказа",
            "description": "Часть заказа возвращена в интернет-магазин, после того как часть заказа была вручена"
        },
        {
            "name": "return-partially-in-progress",
            "title": "Готовится частичный возврат заказа",
            "description": "Часть заказа поехала на возврат, после того как часть заказа была вручена"
        },
        {
            "name": "stored",
            "title": "В пункте самовывоза",
            "description": "Заказ находится в пункте выдачи"
        },
        {
            "name": "unknown",
            "title": "Статус уточняется",
            "description": "Статус заказа уточняется"
        },
        {
            "name": "wait-delivery",
            "title": "Готов к передаче в службу доставки",
            "description": "Заказ готов к передаче в службу доставки"
        }
    ]

    old_work_time_warehouse = {
        "timezone": "+03:00",
        "monday": {
            "from": "09:00",
            "to": "20:00"
        },
        "tuesday": {
            "from": "09:00",
            "to": "20:00"
        },
        "wednesday": {
            "from": "09:00",
            "to": "20:00"
        },
        "thursday": {
            "from": "09:00",
            "to": "20:00"
        },
        "friday": {
            "from": "09:00",
            "to": "20:00"
        },
        "saturday": {
            "from": "09:00",
            "to": "20:00"
        },
        "sunday": {
            "from": "09:00",
            "to": "20:00"
        }
    }

    new_work_time_warehouse = {
        "timezone": "+03:00",
        "monday": {
            "from": "09:00",
            "to": "18:00"
        },
        "tuesday": {
            "from": "09:00",
            "to": "18:00"
        },
        "wednesday": {
            "from": "09:00",
            "to": "18:00"
        },
        "thursday": {
            "from": "09:00",
            "to": "18:00"
        },
        "friday": {
            "from": "09:00",
            "to": "18:00"
        },
        "saturday": {
            "from": "09:00",
            "to": "18:00"
        },
        "sunday": {
            "from": "09:00",
            "to": "18:00"
        }
    }

    details = ["returnItems", "returnReason", "delayReason", "paymentType", "pickupDate", "declaredDeliveryDate",
               "storageDateEnd"]

    rp_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        },
        {
            "code": "10/110",
            "name": "НДС 10/110"
        },
        {
            "code": "20/120",
            "name": "НДС 20/120"
        }
    ]

    rp_services = [
        {
            "name": "no-return",
            "title": "Возврату не подлежит",
            "description": "Возврату не подлежит"
        },
        {
            "name": "open",
            "title": "Можно вскрывать до получения оплаты с клиента",
            "description": "Можно вскрывать до получения оплаты с клиента"
        },
        {
            "name": "pay-by-card",
            "title": "COD (картой или наличными)",
            "description": "COD (картой или наличными)"
        },
        {
            "name": "shelf-life-days",
            "title": "Срок хранения заказа в ОПС",
            "description": "Срок хранения заказа в ОПС"
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя"
        }
    ]

    rp_courier_tariffs = ["24", "7"]

    rp_po_tariffs = ["23", "47", "4"]

    rp_list_tariffs = [
        {
            "id": "24",
            "name": "«Курьер Онлайн»"
        },
        {
            "id": "23",
            "name": "«Посылка Онлайн»"
        },
        {
            "id": "23",
            "name": "«Посылка Онлайн Комбинированный»"
        },
        {
            "id": "47",
            "name": "«Посылка 1 Класса»"
        },
        {
            "id": "4",
            "name": "«Посылка Нестандартная»"
        },
        {
            "id": "7",
            "name": "«EMS»"
        }
    ]

    cdek_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    cdek_services = [
        {
            "name": "dress-fitting",
            "title": "Имеется возможность примерки",
            "description": "Имеется возможность примерки"
         },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)"
         },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)"
         },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)"
         },
        {
            "name": "no-autocall",
            "title": "Отключение автоматического звонка клиенту",
            "description": "Отключение автоматического звонка клиенту"
        },
        {
            "name": "not-open", "title":
            "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента"
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        },
        {
            "name": "reverse",
            "title": "Обратный заказ на доставку от получателя до отправителя",
            "description": "Обратный заказ на доставку от получателя до отправителя"
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя"
        }
    ]

    cdek_courier_tariffs = ["137", "139", "480", "482"]

    cdek_ds_tariffs = ["136", "138", "366", "368", "481", "483", "485", "486"]

    cdek_list_tariffs = [
        {
            "id": "7",
            "name": "«Международный экспресс документы дверь-дверь»"
        },
        {
            "id": "8",
            "name": "«Международный экспресс грузы дверь-дверь»"
        },
        {
            "id": "136",
            "name": "«Посылка склад-склад»"
        },
        {
            "id": "137",
            "name": "«Посылка склад-дверь»"
        },
        {
            "id": "138",
            "name": "«Посылка дверь-склад»"
        },
        {
            "id": "139",
            "name": "«Посылка дверь-дверь»"
        },
        {
            "id": "233",
            "name": "«Экономичная посылка склад-дверь»"
        },
        {
            "id": "234",
            "name": "«Экономичная посылка склад-склад»"
        },
        {
            "id": "291",
            "name": "«CDEK Express склад-склад»"
        },
        {
            "id": "293",
            "name": "«CDEK Express дверь-дверь»"
        },
        {
            "id": "294",
            "name": "«CDEK Express склад-дверь»"
        },
        {
            "id": "295",
            "name": "«CDEK Express дверь-склад»"
        },
        {
            "id": "366",
            "name": "«Посылка дверь-постамат»"
        },
        {
            "id": "368",
            "name": "«Посылка склад-постамат»"
        },
        {
            "id": "378",
            "name": "«Экономичная посылка склад-постамат»"
        },
        {
            "id": "3",
            "name": "«Супер-экспресс до 18 дверь-дверь»"
        },
        {
            "id": "57",
            "name": "«Супер-экспресс до 9 дверь-дверь»"
        },
        {
            "id": "58",
            "name": "«Супер-экспресс до 10 дверь-дверь»"
        },
        {
            "id": "59",
            "name": "«Супер-экспресс до 12 дверь-дверь»"
        },
        {
            "id": "60",
            "name": "«Супер-экспресс до 14 дверь-дверь»"
        },
        {
            "id": "61",
            "name": "«Супер-экспресс до 16 дверь-дверь»"
        },
        {
            "id": "777",
            "name": "«Супер-экспресс до 12 дверь-склад»"
        },
        {
            "id": "786",
            "name": "«Супер-экспресс до 14 дверь-склад»"
        },
        {
            "id": "795",
            "name": "«Супер-экспресс до 16 дверь-склад»"
        },
        {
            "id": "804",
            "name": "«Супер-экспресс до 18 дверь-склад»"
        },
        {
            "id": "778",
            "name": "«Супер-экспресс до 12 склад-дверь»"
        },
        {
            "id": "787",
            "name": "«Супер-экспресс до 14 склад-дверь»"
        },
        {
            "id": "796",
            "name": "«Супер-экспресс до 16 склад-дверь»"
        },
        {
            "id": "805",
            "name": "«Супер-экспресс до 18 склад-дверь»"
        },
        {
            "id": "779",
            "name": "«Супер-экспресс до 12 склад-склад»"
        },
        {
            "id": "788",
            "name": "«Супер-экспресс до 14 склад-склад»"
        },
        {
            "id": "797",
            "name": "«Супер-экспресс до 16 склад-склад»"
        },
        {
            "id": "806",
            "name": "«Супер-экспресс до 18 склад-склад»"
        },
        {
            "id": "62",
            "name": "«Магистральный экспресс склад-склад»"
        },
        {
            "id": "63",
            "name": "«Магистральный супер-экспресс склад-склад»"
        },
        {
            "id": "121",
            "name": "«Магистральный экспресс дверь-дверь»"
        },
        {
            "id": "122",
            "name": "«Магистральный экспресс склад-дверь»"
        },
        {
            "id": "123",
            "name": "«Магистральный экспресс дверь-склад»"
        },
        {
            "id": "124",
            "name": "«Магистральный супер-экспресс дверь-дверь»"
        },
        {
            "id": "125",
            "name": "«Магистральный супер-экспресс склад-дверь»"
        },
        {
            "id": "126",
            "name": "«Магистральный супер-экспресс дверь-склад»"
        },
        {
            "id": "480",
            "name": "«Экспресс дверь-дверь»"
        },
        {
            "id": "481",
            "name": "«Экспресс дверь-склад»"
        },
        {
            "id": "482",
            "name": "«Экспресс склад-дверь»"
        },
        {
            "id": "483",
            "name": "«Экспресс склад-склад»"
        },
        {
            "id": "485",
            "name": "«Экспресс дверь-постамат»"
        },
        {
            "id": "486",
            "name": "«Экспресс склад-постамат»"
        },
        {
            "id": "718",
            "name": "«Супер-экспресс до 18.00 склад-дверь»"
        },
        {
            "id": "719",
            "name": "«Супер-экспресс до 18.00 склад-склад»"
        }
    ]

    boxberry_intervals = [
        {
            "from": "09:00",
            "to": "13:00"
        },
        {
            "from": "12:00",
            "to": "15:00"
        },
        {
            "from": "15:00",
            "to": "18:00"
        },
        {
            "from": "18:00",
            "to": "22:00"
        },
        {
            "from": "09:00",
            "to": "18:00"
        },
        {
            "from": "09:00",
            "to": "15:00"
        },
        {
            "from": "15:00",
            "to": "22:00"
        }
    ]

    boxberry_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    boxberry_services = [
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента"
        },
        {
            "name": "open-test",
            "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности"},
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]

    cse_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "18",
            "name": "НДС 18%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    cse_services = [
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]

    club_intervals = [
        {
            "from": "10:00",
            "to": "14:00"
        },
        {
            "from": "14:00",
            "to": "18:00"
        },
        {
            "from": "18:00",
            "to": "22:00"
        },
        {
            "from": "10:00",
            "to": "18:00"
        }
    ]

    club_vats = [
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    club_services = [
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)"},
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)"},
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)"
        }
    ]

    club_tariffs = ["1", "2", "3", "4", "5", "6", "10", "11"]

    dpd_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    dpd_services = [
        {
            "name": "barcode-generation",
            "title": "Генерация штрихкода на стороне Меташипа",
            "description": "Генерация штрихкода на стороне Меташипа"
        },
        {
            "name": "crate",
            "title": "Обрешётка(защитный каркас) груза",
            "description": "Обрешётка(защитный каркас) груза"
        },
        {
            "name": "dress-fitting",
            "title": "Имеется возможность примерки",
            "description": "Имеется возможность примерки"
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)"
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)"
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)"
        },
        {
            "name": "open",
            "title": "Можно вскрывать до получения оплаты с клиента",
            "description": "Можно вскрывать до получения оплаты с клиента"
        },
        {
            "name": "open-test",
            "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности"
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя"
        },
        {
            "name": "weekend-delivery",
            "title": "Доставка в выходные дни",
            "description": "Доставка в выходные дни"
        },
        {
            "name": "weekend-pickup",
            "title": "Приём в выходные дни",
            "description": "Приём в выходные дни"
        }
    ]

    dpd_courier_tariffs = ["MAX", "NDY", "BZP", "CUR", "ECN", "CSM", "PCL", "IND", "DAY", "MXO"]

    dpd_ds_tariffs = ["BZP", "CUR", "ECN", "CSM", "PCL", "MXO"]

    five_post_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    five_post_services = [
        {
            "name": "no-return",
            "title": "Возврату не подлежит",
            "description": "Возврату не подлежит"
        }
    ]

    topdelivery_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    topdelivery_services = [
        {
            "name": "find-closest-delivery-interval",
            "title": "Поиск ближайшего интервала доставки",
            "description": "Поиск ближайшего интервала доставки"
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)"
        },
        {
            "name": "lifting-freight", "title":
            "Подъем на этаж (грузовой лифт)", "description":
            "Подъем на этаж (грузовой лифт)"
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)"
        },
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента"
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]

    topdelivery_intervals = [
        {
            "from": "10:00",
            "to": "22:00"
        }
    ]

    guru_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    guru_intervals = [
        {
            "from": "10:00",
            "to": "14:00"
        },
        {
            "from": "14:00",
            "to": "18:00"
        },
        {
            "from": "18:00",
            "to": "22:00"
        },
        {
            "from": "10:00",
            "to": "18:00"
        }
    ]

    guru_services = [
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]

    l_post_vats = [
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    l_post_services = [
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)"
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)"
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)"
        },
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента"
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        },
        {
            "name": "return-documents",
            "title": "Возврат документов",
            "description": "Возврат документов"
        }
    ]

    dalli_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    dalli_services = [
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]

    dalli_intervals_1 = [
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "0"
        },
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "2"
        },
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "1"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "1"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "0"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "2"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "0"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "2"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "1"
        },
        {
            "from": "10:00",
            "to": "16:00",
            "zone": "3"
        },
        {
            "from": "10:00",
            "to": "17:00",
            "zone": "2"
        },
        {
            "from": "10:00",
            "to": "17:00",
            "zone": "0"
        },
        {
            "from": "10:00",
            "to": "17:00",
            "zone": "1"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "2"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "4"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "0"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "3"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "1"
        },
        {
            "from": "11:00",
            "to": "15:00",
            "zone": "1"
        },
        {
            "from": "11:00",
            "to": "15:00",
            "zone": "2"
        },
        {
            "from": "11:00",
            "to": "15:00",
            "zone": "0"
        },
        {
            "from": "12:00",
            "to": "22:00",
            "zone": "3"
        },
        {
            "from": "14:00",
            "to": "18:00",
            "zone": "0"
        },
        {
            "from": "14:00",
            "to": "18:00",
            "zone": "2"
        },
        {
            "from": "14:00",
            "to": "18:00",
            "zone": "1"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "0"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "1"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "2"
        }
    ]

    dalli_intervals_2 = [
        {
            "from": "15:00",
            "to": "18:00"
        },
        {
            "from": "18:00",
            "to": "22:00"
        }
    ]

    dalli_intervals_11 = [
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "0"
        },
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "2"
        },
        {
            "from": "08:00",
            "to": "19:00",
            "zone": "1"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "0"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "1"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "0"
        },
        {
            "from": "09:00",
            "to": "13:00",
            "zone": "2"
        },
        {
            "from": "09:00",
            "to": "15:00",
            "zone": "1"
        },
        {
            "from": "09:00",
            "to": "15:00",
            "zone": "2"
        },
        {
            "from": "10:00",
            "to": "17:00",
            "zone": "0"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "2"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "3"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "1"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "4"
        },
        {
            "from": "10:00",
            "to": "22:00",
            "zone": "0"
        },
        {
            "from": "11:00",
            "to": "15:00",
            "zone": "0"
        },
        {
            "from": "14:00",
            "to": "18:00",
            "zone": "0"
        },
        {
            "from": "15:00",
            "to": "21:00",
            "zone": "2"
        },
        {
            "from": "15:00",
            "to": "21:00",
            "zone": "1"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "2"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "0"
        },
        {
            "from": "18:00",
            "to": "22:00",
            "zone": "1"
        }
    ]

    ya_go_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    ya_go_services = [
        {
            "name": "no-recipient-confirmation",
            "title": "Отключение подтверждения кодом для получателя",
            "description": "Отключение подтверждения кодом для получателя"
        },
        {
            "name": "no-sender-confirmation",
            "title": "Отключение подтверждения кодом для отправителя",
            "description": "Отключение подтверждения кодом для отправителя"
        }
    ]

    ya_delivery_vats = [
        {
            "code": "NO_VAT",
            "name": "Без НДС"
        },
        {
            "code": "0",
            "name": "НДС 0%"
        },
        {
            "code": "10",
            "name": "НДС 10%"
        },
        {
            "code": "20",
            "name": "НДС 20%"
        }
    ]

    ya_delivery_services = [
        {
            "name": "barcode-generation",
            "title": "Генерация штрихкода на стороне Меташипа",
            "description": "Генерация штрихкода на стороне Меташипа"
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация"
        }
    ]


INFO = OtherInfo()
