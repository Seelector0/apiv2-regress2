from enum import Enum


class OtherInfo(Enum):

    DETAILS = [
        "returnItems", "returnReason", "delayReason", "paymentType", "pickupDate", "declaredDeliveryDate",
        "storageDateEnd"
    ]

    RP_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"},
        {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"},
        {"code": "10/110", "name": "НДС 10/110"}, {"code": "20/120", "name": "НДС 20/120"}
    ]

    RP_SERVICES = [
        {"name": "no-return", "title": "Возврату не подлежит", "description": "Возврату не подлежит"},
        {"name": "open", "title": "Можно вскрывать до получения оплаты с клиента",
         "description": "Можно вскрывать до получения оплаты с клиента"},
        {"name": "pay-by-card", "title": "COD (картой или наличными)", "description": "COD (картой или наличными)"},
        {"name": "shelf-life-days", "title": "Срок хранения заказа в ОПС", "description": "Срок хранения заказа в ОПС"},
        {"name": "sms", "title": "SMS информирование", "description": "SMS уведомление получателя"}
    ]

    RP_COURIER_TARIFFS = ["24", "7"]

    RP_PO_TARIFFS = ["23", "47", "4"]

    CDEK_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    CDEK_SERVICES = [
        {"name": "lifting-elevator", "title": "Подъем на этаж (лифт)", "description": "Подъем на этаж (лифт)"},
        {"name": "lifting-freight", "title": "Подъем на этаж (грузовой лифт)",
         "description": "Подъем на этаж (грузовой лифт)"},
        {"name": "lifting-manual", "title": "Подъем на этаж (ручной)", "description": "Подъем на этаж (ручной)"},
        {"name": "no-autocall", "title": "Отключение автоматического звонка клиенту", "description":
            "Отключение автоматического звонка клиенту"},
        {"name": "not-open", "title": "Не вскрывать до получения оплаты с клиента",
         "description": "Не вскрывать до получения оплаты с клиента"},
        {"name": "reverse", "title": "Обратный заказ на доставку от получателя до отправителя",
         "description": "Обратный заказ на доставку от получателя до отправителя"}
    ]

    CDEK_COURIER_TARIFFS = ["137", "139", "480", "482"]

    CDEK_DS_TARIFFS = ["136", "138", "366", "368", "481", "483", "485", "486"]

    BOXBERRY_INTERVALS = [
        {"from": "09:00", "to": "13:00"}, {"from": "12:00", "to": "15:00"}, {"from": "15:00", "to": "18:00"},
        {"from": "18:00", "to": "22:00"}, {"from": "09:00", "to": "18:00"}, {"from": "09:00", "to": "15:00"},
        {"from": "15:00", "to": "22:00"}
    ]

    BOXBERRY_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    BOXBERRY_SERVICES = [
        {"name": "not-open", "title": "Не вскрывать до получения оплаты с клиента",
         "description": "Не вскрывать до получения оплаты с клиента"},
        {"name": "open-test",  "title": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности",
         "description": "Можно вскрывать до получения оплаты с клиента для проверки работоспособности"},
        {"name": "partial-sale", "title": "Частичная реализация", "description": "Частичная реализация"}
    ]

    CSE_VATS = [
        {'code': 'NO_VAT', 'name': 'Без НДС'}, {'code': '0', 'name': 'НДС 0%'}, {'code': '10', 'name': 'НДС 10%'},
        {'code': '18', 'name': 'НДС 18%'}, {'code': '20', 'name': 'НДС 20%'}
    ]

    CSE_SERVICES = [
        {'name': 'partial-sale', 'title': 'Частичная реализация', 'description': 'Частичная реализация'}
    ]

    CLUB_INTERVALS = [
        {'from': '10:00', 'to': '14:00'}, {'from': '14:00', 'to': '18:00'}, {'from': '18:00', 'to': '22:00'},
        {'from': '10:00', 'to': '18:00'}
    ]

    CLUB_VATS = [
        {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"}
    ]

    CLUB_SERVICES = [
        {"name": "lifting-elevator", "title": "Подъем на этаж (лифт)", "description": "Подъем на этаж (лифт)"},
        {"name": "lifting-freight", "title": "Подъем на этаж (грузовой лифт)",
         "description": "Подъем на этаж (грузовой лифт)"},
        {"name": "lifting-manual", "title": "Подъем на этаж (ручной)", "description": "Подъем на этаж (ручной)"}
    ]

    CLUB_TARIFFS = ["1", "2", "3", "4", "5", "6", "10", "11"]

    DPD_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    DPD_SERVICES = [
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

    DPD_COURIER_TARIFFS = ["MAX", "NDY", "BZP", "CUR", "ECN", "CSM", "PCL", "IND", "DAY", "MXO"]

    DPD_DS_TARIFFS = ["BZP", "CUR", "ECN", "CSM", "PCL", "MXO"]

    FIVE_POST_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "10", "name": "НДС 10%"}, {"code": "20", "name": "НДС 20%"}
    ]

    TOPDELIVERY_VATS = [
        {'code': 'NO_VAT', 'name': 'Без НДС'}, {'code': '0', 'name': 'НДС 0%'}, {'code': '10', 'name': 'НДС 10%'},
        {'code': '20', 'name': 'НДС 20%'}
    ]

    TOPDELIVERTY_SERVICES = [
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

    GURU_VATS = [
        {"code": "NO_VAT", "name": "Без НДС"}, {"code": "0", "name": "НДС 0%"}, {"code": "10", "name": "НДС 10%"},
        {"code": "20", "name": "НДС 20%"}
    ]

    GURU_INTERVALS = [
        {"from": "10:00", "to": "14:00"}, {"from": "14:00", "to": "18:00"}, {"from": "18:00", "to": "22:00"},
        {"from": "10:00", "to": "18:00"}
    ]

    GURU_SERVICES = [
        {"name": "partial-sale", "title": "Частичная реализация", "description": "Частичная реализация"}
    ]
