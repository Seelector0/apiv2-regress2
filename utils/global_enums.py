class OtherInfo:
    created_entity = ["id", "type", "url", "status"]

    entity_shops = ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"]

    entity_warehouse = ["id", "number", "name", "visibility", "address", "contact", "workingTime", "pickup",
                        "dpdPickupNum", "lPostWarehouseId", "yandexWarehouseId", "comment"]

    entity_order = ["id", "number", "addressTo", "data", "parcel", "status", "statusReason", "state", "stateMessage",
                    "created", "configurationType"]

    entity_parcel = ["id", "number", "shop", "deliveryServiceCode", "data", "created", "deleted", "state", "stateTime"]

    entity_intake = ["id", "number", "deliveryServiceId", "status", "createdAt", "request"]

    created_entity_widget = ["id", "customerId", "shopId", "token", "createdAt", "updatedAt"]

    entity_widget = ["id", "customerId", "shopId", "token", "script", "createdAt", "updatedAt"]

    entity_moderation = ["id", "connectionId", "agreementId", "customerAgreementId", "credential", "notified",
                         "expired"]

    entity_webhook = ["id", "shopId", "url", "name", "secret", "eventType", "active", "createdAt", "updatedAt"]

    entity_forms_parcels_labels = ["id", "state", "type", "data", "artifacts", "createdAt", "stateTime", "message"]

    entity_connections_id = ["id", "shopId", "deliveryService", "data"]

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
            "name": "fragile",
            "title": "Хрупкое",
            "description": "Хрупкое",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "no-return",
            "title": "Возврату не подлежит",
            "description": "Возврату не подлежит",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "open",
            "title": "Можно вскрывать до получения оплаты с клиента",
            "description": "Можно вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "pay-by-card",
            "title": "COD (картой или наличными)",
            "description": "COD (картой или наличными)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "shelf-life-days",
            "title": "Срок хранения заказа в ОПС",
            "description": "Срок хранения заказа в ОПС",
            "options": {
                "hasParameter": True
            }
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя",
            "options": {
                "hasParameter": False
            }
        }
    ]

    rp_courier_tariffs = ["24", "7"]

    rp_po_tariffs = ["23", "47", "4"]

    rp_dp_tariffs = ["54"]

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
        },
        {
            "id": "54",
            "name": "«ЕКОМ Маркетплейс»"
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

    cdek_services = [
        {
            "name": "dress-fitting",
            "title": "Имеется возможность примерки",
            "description": "Имеется возможность примерки",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "no-autocall",
            "title": "Отключение автоматического звонка клиенту",
            "description": "Отключение автоматического звонка клиенту",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "not-open", "title":
            "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "reverse",
            "title": "Обратный заказ на доставку от получателя до отправителя",
            "description": "Обратный заказ на доставку от получателя до отправителя",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя",
            "options": {
                "hasParameter": False
            }
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
        },
        {
            "id": "748",
            "name": "«Сборный груз дверь-дверь»"
        },
        {
            "id": "749",
            "name": "«Сборный груз дверь-склад»"
        },
        {
            "id": "750",
            "name": "«Сборный груз склад-дверь»"
        },
        {
            "id": "751",
            "name": "«Сборный груз склад-склад»"
        },
        {
            "id": "2360",
            "name": "«Доставка день в день»"
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

    boxberry_services = [
        {
            "name": "dress-fitting",
            "title": "Имеется возможность примерки",
            "description": "Имеется возможность примерки",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "open-test",
            "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
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
            "name": "fragile",
            "title": "Хрупкое",
            "description": "Хрупкое",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
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
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
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
            "description": "Генерация штрихкода на стороне Меташипа",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "crate",
            "title": "Обрешётка(защитный каркас) груза",
            "description": "Обрешётка(защитный каркас) груза",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "dress-fitting",
            "title": "Имеется возможность примерки",
            "description": "Имеется возможность примерки",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "open",
            "title": "Можно вскрывать до получения оплаты с клиента",
            "description": "Можно вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "open-test",
            "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "temperature-restrictions",
            "title": "Температурный режим",
            "description": "Температурный режим",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "weekend-delivery",
            "title": "Доставка в выходные дни",
            "description": "Доставка в выходные дни",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "weekend-pickup",
            "title": "Приём в выходные дни",
            "description": "Приём в выходные дни",
            "options": {
                "hasParameter": False
            }
        }
    ]

    dpd_ds_tariffs = ["NDY", "CUR", "ECN", "CSM", "PCL", "MXO"]

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
            "description": "Возврату не подлежит",
            "options": {
                "hasParameter": False
            }
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
            "description": "Поиск ближайшего интервала доставки",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight", "title":
            "Подъем на этаж (грузовой лифт)", "description":
            "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
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
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "return-documents",
            "title": "Возврат документов",
            "description": "Возврат документов",
            "options": {
                "hasParameter": False
            }
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

    dalli_services = [
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
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
            "description": "Отключение подтверждения кодом для получателя",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "no-sender-confirmation",
            "title": "Отключение подтверждения кодом для отправителя",
            "description": "Отключение подтверждения кодом для отправителя",
            "options": {
                "hasParameter": False
            }
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

    ya_delivery_services = [
        {
            "name": "barcode-generation",
            "title": "Генерация штрихкода на стороне Меташипа",
            "description": "Генерация штрихкода на стороне Меташипа",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "partial-sale",
            "title": "Частичная реализация",
            "description": "Частичная реализация",
            "options": {
                "hasParameter": False
            }
        }
    ]

    halva_vats = [
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

    pecom_services = [
        {
            "name": "crate",
            "title": "Обрешётка(защитный каркас) груза",
            "description": "Обрешётка(защитный каркас) груза",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-elevator",
            "title": "Подъем на этаж (лифт)",
            "description": "Подъем на этаж (лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-freight",
            "title": "Подъем на этаж (грузовой лифт)",
            "description": "Подъем на этаж (грузовой лифт)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "lifting-manual",
            "title": "Подъем на этаж (ручной)",
            "description": "Подъем на этаж (ручной)",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "reverse",
            "title": "Обратный заказ на доставку от получателя до отправителя",
            "description": "Обратный заказ на доставку от получателя до отправителя",
            "options": {
                "hasParameter": False
            }
        },
        {
            "name": "strapping",
            "title": "Упаковка стреппинг-лентой",
            "description": "Упаковка стреппинг-лентой",
            "options": {
                "hasParameter": False
            }
        }
    ]

    pecom_vats = [
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

    ds_kazakhstan_services = [
        {
            "name": "sms",
            "title": "SMS информирование",
            "description": "SMS уведомление получателя",
            "options": {
                "hasParameter": False
            }
        }
    ]


INFO = OtherInfo()
