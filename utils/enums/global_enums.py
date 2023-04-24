

class OtherInfo:

    created_entity = ["id", "type", "url", "status"]

    details = [
        "returnItems", "returnReason", "delayReason", "paymentType", "pickupDate", "declaredDeliveryDate",
        "storageDateEnd"
    ]

    rp_vats = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"},
        {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"},
        {"code": "10/110", "name": "НДС 10/110"}, {"code": "20/120", "name": "НДС 20/120"}
    ]

    rp_services = [
        {"name": "no-return", "title": "Возврату не подлежит", "description": "Возврату не подлежит"},
        {"name": "open", "title": "Можно вскрывать до получения оплаты с клиента",
         "description": "Можно вскрывать до получения оплаты с клиента"},
        {"name": "pay-by-card", "title": "COD (картой или наличными)", "description": "COD (картой или наличными)"},
        {"name": "shelf-life-days", "title": "Срок хранения заказа в ОПС", "description": "Срок хранения заказа в ОПС"},
        {"name": "sms", "title": "SMS информирование", "description": "SMS уведомление получателя"}
    ]

    rp_courier_tariffs = ["24", "7"]

    rp_po_tariffs = ["23", "47", "4"]

    cdek_vats = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
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
            "name": "not-open",
            "title": "Не вскрывать до получения оплаты с клиента",
            "description": "Не вскрывать до получения оплаты с клиента"
        },
        {
            "name": "reverse",
            "title": "Обратный заказ на доставку от получателя до отправителя",
            "description": "Обратный заказ на доставку от получателя до отправителя"
        }
    ]

    cdek_courier_tariffs = ["137", "139", "480", "482"]

    cdek_ds_tariffs = ["136", "138", "366", "368", "481", "483", "485", "486"]

    boxberry_intervals = [
        {"from": "09:00", "to": "13:00"}, {"from": "12:00", "to": "15:00"}, {"from": "15:00", "to": "18:00"},
        {"from": "18:00", "to": "22:00"}, {"from": "09:00", "to": "18:00"}, {"from": "09:00", "to": "15:00"},
        {"from": "15:00", "to": "22:00"}
    ]

    boxberry_vats = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    boxberry_services = [
        {"name": "not-open", "title": "Не вскрывать до получения оплаты с клиента",
         "description": "Не вскрывать до получения оплаты с клиента"},
        {"name": "open-test",  "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
         "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности"},
        {"name": "partial-sale", "title": "Частичная реализация", "description": "Частичная реализация"}
    ]

    cse_vats = [
        {'code': 'NO_VAT', 'name': 'Без НДС'}, {'code': '0', 'name': 'НДС 0%'}, {'code': '10', 'name': 'НДС 10%'},
        {'code': '18', 'name': 'НДС 18%'}, {'code': '20', 'name': 'НДС 20%'}
    ]

    cse_services = [
        {'name': 'partial-sale', 'title': 'Частичная реализация', 'description': 'Частичная реализация'}
    ]

    club_intervals = [
        {'from': '10:00', 'to': '14:00'}, {'from': '14:00', 'to': '18:00'}, {'from': '18:00', 'to': '22:00'},
        {'from': '10:00', 'to': '18:00'}
    ]

    club_vats = [
        {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"}
    ]

    club_services = [
        {"name": "lifting-elevator", "title": "Подъем на этаж (лифт)", "description": "Подъем на этаж (лифт)"},
        {"name": "lifting-freight", "title": "Подъем на этаж (грузовой лифт)",
         "description": "Подъем на этаж (грузовой лифт)"},
        {"name": "lifting-manual", "title": "Подъем на этаж (ручной)", "description": "Подъем на этаж (ручной)"}
    ]

    club_tariffs = ["1", "2", "3", "4", "5", "6", "10", "11"]

    dpd_vats = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    dpd_services = [
        {'name': 'barcode-generation', 'title': 'Генерация штрихкода на стороне Меташипа',
         'description': 'Генерация штрихкода на стороне Меташипа'},
        {'name': 'dress-fitting', 'title': 'Имеется возможность примерки',
         'description': 'Имеется возможность примерки'},
        {'name': 'open', 'title': 'Можно вскрывать до получения оплаты с клиента',
         'description': 'Можно вскрывать до получения оплаты с клиента'},
        {'name': 'open-test', 'title': 'Можно вскрывать до получения оплаты с клиента для проверки работоспособности',
         'description': 'Можно вскрывать до получения оплаты с клиента для проверки работоспособности'},
        {'name': 'partial-sale', 'title': 'Частичная реализация', 'description': 'Частичная реализация'},
        {'name': 'sms', 'title': 'SMS информирование', 'description': 'SMS уведомление получателя'},
        {'name': 'weekend-delivery', 'title': 'Доставка в выходные дни', 'description': 'Доставка в выходные дни'},
        {'name': 'weekend-pickup', 'title': 'Приём в выходные дни', 'description': 'Приём в выходные дни'}
    ]

    dpd_courier_tariffs = ["MAX", "NDY", "BZP", "CUR", "ECN", "CSM", "PCL", "IND", "DAY", "MXO"]

    dpd_ds_tariffs = ["BZP", "CUR", "ECN", "CSM", "PCL", "MXO"]

    FIVE_POST_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"}
    ]

    topdelivery_vats = [
        {'code': 'NO_VAT', 'name': 'Без НДС'}, {'code': '0', 'name': 'НДС 0%'}, {'code': '10', 'name': 'НДС 10%'},
        {'code': '20', 'name': 'НДС 20%'}
    ]

    topdelivery_services = [
        {'name': 'find-closest-delivery-interval', 'title': 'Поиск ближайшего интервала доставки',
         'description': 'Поиск ближайшего интервала доставки'},
        {'name': 'lifting-elevator', 'title': 'Подъем на этаж (лифт)', 'description': 'Подъем на этаж (лифт)'},
        {'name': 'lifting-freight', 'title': 'Подъем на этаж (грузовой лифт)',
         'description': 'Подъем на этаж (грузовой лифт)'},
        {'name': 'lifting-manual', 'title': 'Подъем на этаж (ручной)', 'description': 'Подъем на этаж (ручной)'},
        {'name': 'not-open', 'title': 'Не вскрывать до получения оплаты с клиента',
         'description': 'Не вскрывать до получения оплаты с клиента'},
        {'name': 'partial-sale', 'title': 'Частичная реализация', 'description': 'Частичная реализация'}
    ]

    guru_vats = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    guru_intervals = [
        {"from": "10:00", "to": "14:00"}, {"from": "14:00", "to": "18:00"}, {"from": "18:00", "to": "22:00"},
        {"from": "10:00", "to": "18:00"}
    ]

    guru_services = [
        {"name": "partial-sale", "title": "Частичная реализация", "description": "Частичная реализация"}
    ]


INFO = OtherInfo()
