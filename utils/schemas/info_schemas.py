class InfoSchema:
    info_vat = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "enum": ["NO_VAT", "0", "5", "7", "10", "18", "20", "10/110", "20/120"],
                    "description": "Код НДС"
                },
                "name": {
                    "type": "string",
                    "description": "Название типа НДС"
                }
            },
            "required": ["code", "name"],
            "additionalProperties": False
        }
    }

    info_intake_office = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Код точки сдачи"
                },
                "name": {
                    "type": "string",
                    "description": "Наименование точки сдачи"
                },
                "deliveryServiceCode": {
                    "type": "string",
                    "enum": ["RussianPost", "TopDelivery", "Cdek", "Boxberry", "Dpd", "Cse", "FivePost", "YandexGo",
                             "YandexDelivery", "DostavkaClub", "Dalli", "LPost", "Halva", "Pecom"],
                    "description": "Код службы доставки"
                }
            },
            "required": ["code", "name", "deliveryServiceCode"],
            "additionalProperties": False
        }
    }

    info_tariff = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор тарифа в СД"
                },
                "name": {
                    "type": "string",
                    "description": "Наименование тарифа в СД"
                }
            },
            "required": ["id", "name"],
            "additionalProperties": False
        }
    }

    info_service = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "enum": ["barcode-generation", "dress-fitting", "find-closest-delivery-interval", "fragile",
                             "lifting-elevator", "lifting-freight", "lifting-manual", "no-autocall",
                             "no-recipient-confirmation", "no-return", "no-sender-confirmation", "not-open", "open",
                             "open-test", "partial-sale", "pay-by-card", "reverse", "shelf-life-days", "sms",
                             "strapping", "temperature-restrictions", "weekend-delivery", "weekend-pickup",
                             "on-demand", "safe-deal", "return-documents", "crate"],
                    "description": "Название услуги"
                },
                "title": {
                    "type": "string",
                    "description": "Наименование услуги"
                },
                "description": {
                    "type": "string",
                    "description": "Описание услуги"
                },
                "options": {
                    "type": "object",
                    "properties": {
                        "hasParameter": {
                            "type": "boolean",
                            "description": "Флаг, указывающий на возможность передачи параметра"
                        }
                    },
                    "required": ["hasParameter"],
                    "additionalProperties": False
                }
            },
            "required": ["name", "title", "description", "options"],
            "additionalProperties": False
        }
    }

    info_schedule = {
        "type": "object",
        "properties": {
            "schedule": {
                "type": "string",
                "enum": ["intervals"],
                "description": "Идентификатор созданного объекта"
            },
            "intervals": {
                "type": "array",
                "minItems": 2,
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {
                            "type": "string",
                            "format": "time",
                            "description": "Флаг, указывающий на возможность передачи параметра"
                        },
                        "to": {
                            "type": "string",
                            "format": "time",
                            "description": "Флаг, указывающий на возможность передачи параметра"
                        },
                        "zone": {
                            "type": "string",
                            "description": "Флаг, указывающий на возможность передачи параметра"
                        },
                        "date": {
                            "type": ["string", "null"],
                            "format": "date",
                            "description": "Флаг, указывающий на возможность передачи параметра"
                        }
                    },
                    "required": ["from", "to", "date"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["schedule", "intervals"],
        "additionalProperties": False
    }

    info_clients = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Наименование"
                },
                "id": {
                    "type": "string",
                    "description": "Токен"
                },
                "secret": {
                    "type": "string",
                    "description": "Секретный код"
                },
                "active": {
                    "type": "boolean",
                    "description": "Статус"
                },
                "created": {
                    "type": "string",
                    "description": "Дата и время создания"
                }
            },
            "required": ["name", "id", "secret", "active", "created"],
            "additionalProperties": False
        }
    }

    info_client_by_id = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Наименование"
            },
            "id": {
                "type": "string",
                "description": "Токен"
            },
            "secret": {
                "type": "string",
                "description": "Секретный код"
            },
            "active": {
                "type": "boolean",
                "description": "Статус"
            },
            "created": {
                "type": "string",
                "format": "date-time",
                "description": "Дата и время создания"
            }
        },
        "required": ["name", "id", "secret", "active", "created"],
        "additionalProperties": False
    }

    info_address = {
        "type": "object",
        "properties": {
            "raw": {
                "type": "string",
                "description": "Исходная адресная строка"
            },
            "postCode": {
                "type": "string",
                "description": "Почтовый индекс"
            }
        },
        "required": ["raw", "postCode"],
        "additionalProperties": False
    }

    info_delivery_service_point = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "deliveryServiceCode": {
                    "type": "string",
                    "enum": ["RussianPost", "TopDelivery", "Cdek", "Boxberry", "Dpd", "Cse", "FivePost", "YandexGo",
                             "YandexDelivery", "Dalli", "LPost", "Halva", "Pecom"],
                    "description": "Код службы доставки"
                },
                "externalDeliveryCode": {
                    "type": ["string", "null"],
                    "description": "Внешний код доставки"
                },
                "deliveryServiceNumber": {
                    "type": "string",
                    "description": "Код ПВЗ"
                },
                "type": {
                    "type": "string",
                    "enum": ["pickup", "terminal", "post"],
                    "description": "Тип ПВЗ"
                },
                "workTime": {
                    "type": "object",
                    "properties": {
                        "raw": {
                            "type": ["string", "null"],
                            "description": "Неформатированое время работы, полученное от СД"
                        },
                        "parsed": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "day": {
                                        "type": "integer",
                                        "description": "Номер дня недели, когда ПВЗ работает"
                                    },
                                    "workTimes": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "start": {
                                                    "type": "string",
                                                    "description": "Время начала"
                                                },
                                                "end": {
                                                    "type": "string",
                                                    "description": "Время конца"
                                                }
                                            },
                                            "required": ["start", "end"],
                                            "additionalProperties": False
                                        },
                                        "description": "Временные периоды в которые ПВЗ работает в этот день"
                                    }
                                },
                                "required": ["day", "workTimes"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["raw", "parsed"],
                    "additionalProperties": False
                },
                "isOnlyPrepaid": {
                    "type": ["boolean", "null"],
                    "description": "Только по предоплате"
                },
                "isCashAllowed": {
                    "type": ["boolean", "null"],
                    "description": "Оплата наличными"
                },
                "isAcquiringAvailable": {
                    "type": ["boolean", "null"],
                    "description": "Оплата картой"
                },
                "name": {
                    "type": "string",
                    "description": "Название ПВЗ"
                },
                "comment": {
                    "type": ["string", "null"],
                    "description": "Комментарий"
                },
                "phone": {
                    "type": ["string", "null"],
                    "description": "Телефон"
                },
                "address": {
                    "type": "object",
                    "properties": {
                        "postalCode": {
                            "type": ["string", "null"],
                            "description": "Почтовый индекс"
                        },
                        "city": {
                            "type": ["string", "null"],
                            "description": "Город"
                        },
                        "settlement": {
                            "type": ["string", "null"],
                            "description": "Населённый пункт"
                        },
                        "region": {
                            "type": ["string", "null"],
                            "description": "Регион"
                        },
                        "street": {
                            "type": ["string", "null"],
                            "description": "Улица"
                        },
                        "house": {
                            "type": ["string", "null"],
                            "description": "Дом"
                        },
                        "building": {
                            "type": ["string", "null"],
                            "description": "Корпус"
                        },
                        "apartment": {
                            "type": ["string", "null"],
                            "description": "Квартира"
                        },
                        "raw": {
                            "type": "string",
                            "description": "Полный адрес"
                        },
                        "latitude": {
                            "type": "number",
                            "description": "Широта"
                        },
                        "longitude": {
                            "type": "number",
                            "description": "Долгота"
                        },
                        "fias": {
                            "type": ["string", "null"],
                            "description": "Фиас"
                        },
                        "deliveryService": {
                            "type": "array",
                            "items": {
                                "type": "object"
                            },
                            "description": "Службы доставки"
                        }
                    },
                    "required": ["postalCode", "city", "region", "street", "house", "raw", "latitude", "longitude",
                                 "fias"],
                    "additionalProperties": False
                },
                "issues": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    },
                    "description": "Известные особенности точки ПВЗ"
                },
                "extraType": {
                    "type": ["string", "null"],
                    "description": "Наименование торговой сети"
                },
                "services": {
                    "type": "array",
                    "items": {
                        "type": ["object", "string"],
                    },
                    "description": "Сервисы ПВЗ"
                },
                "restrictions": {
                    "type": ["object", "null"],
                    "properties": {
                        "maxWeight": {
                            "type": ["number", "null"],
                            "description": "Максимальный вес"
                        },
                        "maxHeight": {
                            "type": ["number", "null"],
                            "description": "Максимальная высота"
                        },
                        "maxLength": {
                            "type": ["number", "null"],
                            "description": "Максимальная длина"
                        },
                        "maxWidth": {
                            "type": ["number", "null"],
                            "description": "Максимальная ширина"
                        },
                        "maxDeclaredCost": {
                            "type": ["number", "null"],
                            "description": "Максимальная объявленная стоимость"
                        }
                    },
                    "required": ["maxWeight", "maxHeight", "maxLength", "maxWidth", "maxDeclaredCost"],
                    "additionalProperties": False
                },
                "photos": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Ссылки на фотографии"
                },
                "deliveryServiceFields": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    },
                    "description": "Поля службы доставки"
                },
                "shelfLifeDays": {
                    "type": ["integer", "null"],
                    "description": "Срок хранения"
                }
            },
            "required": ["deliveryServiceCode", "externalDeliveryCode", "deliveryServiceNumber", "type", "workTime",
                         "isOnlyPrepaid", "isCashAllowed", "isAcquiringAvailable", "name", "comment", "phone",
                         "address", "issues", "extraType", "services", "restrictions", "photos",
                         "deliveryServiceFields", "shelfLifeDays"],
            "additionalProperties": False
        }
    }
