class OrderSchema:
    order_create = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор созданного заказа в системе MetaShip"
            },
            "type": {
                "type": "string",
                "enum": ["Order"],
                "description": "Тип созданного объекта: всегда order"
            },
            "url": {
                "type": "string",
                "format": "uri",
                "description": "Ссылка для получения информации о созданном объекте"
            },
            "status": {
                "type": "integer",
                "enum": [201],
                "description": "HTTP-статус ответа"
            }
        },
        "required": ["id", "type", "url", "status"],
        "additionalProperties": False
    }

    order_create_from_file = {
        "type": "object",
        "patternProperties": {
            "^\\d+$": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Идентификатор созданного заказа в системе MetaShip"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Order"],
                        "description": "Тип созданного объекта: всегда order"
                    },
                    "url": {
                        "type": "string",
                        "format": "uri",
                        "description": "Ссылка для получения информации о созданном объекте"
                    },
                    "status": {
                        "type": "integer",
                        "description": "HTTP-статус ответа"
                    }
                },
                "required": ["id", "type", "url", "status"],
                "additionalProperties": False
            }
        }
    }

    order_get = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Уникальный идентификатор заказа"
                },
                "number": {
                    "type": "string",
                    "description": "Номер заказа "
                },
                "addressTo": {
                    "type": ["object", "null"],
                    "properties": {
                        "raw": {
                            "type": ["string", "null"],
                            "description": "Адрес одной строкой"
                        }
                    }
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "object",
                            "properties": {
                                "warehouse": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Идентификатор склада"
                                        }
                                    },
                                    "required": ["id"]
                                },
                                "shop": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "Идентификатор магазина"
                                        },
                                        "number": {
                                            "type": "string",
                                            "description": "Номер магазина"
                                        },
                                        "barcode": {
                                            "type": ["string", "null"],
                                            "description": "Штрихкод магазина (может быть пустым)"
                                        }
                                    },
                                    "required": ["id", "number", "barcode"]
                                },
                                "payment": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["Paid", "PayOnDelivery"],
                                            "description": "Тип оплаты"
                                        },
                                        "declaredValue": {
                                            "type": "number",
                                            "description": "Объявленная стоимость"
                                        },
                                        "deliverySum": {
                                            "type": "number",
                                            "description": "Сумма доставки"
                                        }
                                    },
                                    "required": ["type", "declaredValue", "deliverySum"]
                                },
                                "dimension": {
                                    "type": ["object", "null"],
                                    "description": "Габариты",
                                    "properties": {
                                        "length": {
                                            "type": "number",
                                            "description": "Длина"
                                        },
                                        "width": {
                                            "type": "number",
                                            "description": "Ширина"
                                        },
                                        "height": {
                                            "type": "number",
                                            "description": "Высота"
                                        }
                                    },
                                    "required": ["length", "width", "height"]
                                },
                                "weight": {
                                    "type": "number",
                                    "description": "Вес заказа"
                                },
                                "delivery": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["Courier", "DeliveryPoint", "PostOffice"],
                                            "description": "Тип доставки"
                                        },
                                        "service": {
                                            "type": "string",
                                            "description": "Служба доставки"
                                        },
                                        "tariff": {
                                            "type": ["string", "null"],
                                            "description": "Тариф доставки"
                                        },
                                        "deliveryPointCode": {
                                            "type": ["string", "null"],
                                            "description": "Код точки доставки"
                                        },
                                        "date": {
                                            "type": ["string", "null"],
                                            "description": "Дата доставки"
                                        },
                                        "time": {
                                            "type": ["object", "null"],
                                            "properties": {
                                                "from": {
                                                    "type": ["string", "null"],
                                                    "description": "Время начала доставки"
                                                },
                                                "to": {
                                                    "type": ["string", "null"],
                                                    "description": "Время окончания доставки"
                                                }
                                            },
                                            "description": "Время доставки"
                                        },
                                        "partner": {
                                            "type": ["string", "null"],
                                            "description": "Партнер доставки"
                                        },
                                        "intakePointCode": {
                                            "type": ["string", "null"],
                                            "description": "Код точки сдачи"
                                        }
                                    },
                                    "required": ["type", "service", "tariff", "deliveryPointCode", "date", "time",
                                                 "partner", "intakePointCode"]
                                },
                                "recipient": {
                                    "type": "object",
                                    "properties": {
                                        "familyName": {
                                            "type": ["string", "null"],
                                            "description": "Фамилия"
                                        },
                                        "firstName": {
                                            "type": ["string", "null"],
                                            "description": "Имя"
                                        },
                                        "secondName": {
                                            "type": ["string", "null"],
                                            "description": "Отчество"
                                        },
                                        "fullName": {
                                            "type": ["string", "null"],
                                            "description": "Полное имя"
                                        },
                                        "phoneNumber": {
                                            "type": ["string", "null"],
                                            "description": "Номер телефона"
                                        },
                                        "email": {
                                            "type": ["string", "null"],
                                            "description": "Электронная почта"
                                        },
                                        "address": {
                                            "type": "object",
                                            "properties": {
                                                "raw": {
                                                    "type": ["string", "null"],
                                                    "description": "Адрес"
                                                },
                                                "countryCode": {
                                                    "type": ["string", "null"],
                                                    "description": "Код страны"
                                                }
                                            },
                                            "required": ["raw", "countryCode"]
                                        },
                                        "additionalPhones": {
                                            "type": "array",
                                            "items": {
                                                "type": ["string", "null"]
                                            },
                                            "description": "Дополнительные телефоны"
                                        }
                                    },
                                    "required": ["familyName", "firstName", "secondName", "fullName", "phoneNumber",
                                                 "email", "address", "additionalPhones"]
                                },
                                "datePickup": {
                                    "type": ["string", "null"],
                                    "description": "Дата привоза на склад"
                                },
                                "pickupTimePeriod": {
                                    "type": ["string", "null"],
                                    "description": "Интервал привоза на склад"
                                },
                                "comment": {
                                    "type": ["string", "null"],
                                    "description": "Комментарий"
                                },
                                "places": {
                                    "type": ["array", "null"],
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "items": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "article": {
                                                            "type": "string",
                                                            "description": "Артикул товара"
                                                        },
                                                        "name": {
                                                            "type": "string",
                                                            "description": "Название товара"
                                                        },
                                                        "price": {
                                                            "type": "number",
                                                            "description": "Цена товара"
                                                        },
                                                        "declaredValue": {
                                                            "type": ["number", "null"],
                                                            "description": "Объявленная стоимость товара"
                                                        },
                                                        "count": {
                                                            "type": "integer",
                                                            "description": "Количество товара"
                                                        },
                                                        "weight": {
                                                            "type": ["number", "null"],
                                                            "description": "Вес товара"
                                                        },
                                                        "vat": {
                                                            "type": "string",
                                                            "description": "НДС товара"
                                                        },
                                                        "barcode": {
                                                            "type": ["string", "null"],
                                                            "description": "Штрихкод товара"
                                                        },
                                                        "marking": {
                                                            "type": ["string", "null"],
                                                            "description": "Маркировка товара"
                                                        },
                                                        "groupMarking": {
                                                            "type": ["string", "null"],
                                                            "description": "Групповая маркировка товара"
                                                        },
                                                        "type": {
                                                            "type": ["string", "null"],
                                                            "description": "Тип товара"
                                                        },
                                                        "supplier": {
                                                            "type": ["string", "null"],
                                                            "description": "Поставщик товара"
                                                        }
                                                    },
                                                    "required": ["article", "name", "price", "declaredValue", "count",
                                                                 "weight", "vat", "barcode", "marking", "groupMarking",
                                                                 "type", "supplier"]
                                                }
                                            },
                                            "barcode": {
                                                "type": ["string", "null"],
                                                "description": "Штрихкод для места"
                                            },
                                            "shopNumber": {
                                                "type": ["string", "null"],
                                                "description": "Уникальный номер грузоместа в ИМ"
                                            },
                                            "weight": {
                                                "type": ["number", "null"],
                                                "description": "Вес места"
                                            },
                                            "dimension": {
                                                "type": ["object", "null"],
                                                "properties": {
                                                    "length": {
                                                        "type": "number",
                                                        "description": "Длина места"
                                                    },
                                                    "width": {
                                                        "type": "number",
                                                        "description": "Ширина места"
                                                    },
                                                    "height": {
                                                        "type": "number",
                                                        "description": "Высота места"
                                                    }
                                                },
                                                "required": ["length", "width", "height"]
                                            }
                                        },
                                        "required": ["items", "barcode", "shopNumber", "weight", "dimension"]
                                    }
                                },
                                "services": {
                                    "type": ["array", "null"],
                                    "items": {
                                        "type": ["string", "null"]
                                    },
                                    "description": "Дополнительные услуги"
                                }
                            },
                            "required": ["warehouse", "shop", "payment", "dimension", "weight", "delivery", "recipient",
                                         "datePickup", "pickupTimePeriod", "comment", "places", "services"]
                        },
                        "deliveryService": {
                            "type": ["object", "null"],
                            "properties": {
                                "id": {
                                    "type": ["string", "null"],
                                    "description": "Идентификатор службы доставки"
                                },
                                "trackingNumber": {
                                    "type": ["string", "null"],
                                    "description": "Номер отслеживания"
                                },
                                "baseRate": {
                                    "type": ["number", "null"],
                                    "description": "Основной тариф"
                                },
                                "insrValueWithVat": {
                                    "type": ["number", "null"],
                                    "description": "Страховая стоимость с НДС"
                                },
                                "esppCode": {
                                    "type": ["string", "null"],
                                    "description": "Код ESPP"
                                },
                                "weight": {
                                    "type": ["number", "null"],
                                    "description": "Вес"
                                },
                                "dimensions": {
                                    "type": ["object", "null"],
                                    "properties": {
                                        "length": {
                                            "type": ["number", "null"],
                                            "description": "Длина"
                                        },
                                        "width": {
                                            "type": ["number", "null"],
                                            "description": "Ширина"
                                        },
                                        "height": {
                                            "type": ["number", "null"],
                                            "description": "Высота"
                                        }
                                    },
                                    "description": "Габариты"
                                }
                            },
                            "required": ["id", "trackingNumber", "baseRate", "insrValueWithVat", "esppCode",
                                         "weight", "dimensions"]
                        }
                    },
                    "required": ["request", "deliveryService"]
                },
                "parcel": {
                    "type": ["object", "null"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Идентификатор партии"
                        }
                    },
                    "required": ["id"],
                    "description": "Информация о партии"
                },
                "status": {
                    "type": "string",
                    "enum": ["created", "wait-delivery"],
                    "description": "Статус заказа"
                },
                "statusTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Время изменения статуса"
                },
                "state": {
                    "type": "string",
                    "enum": ["registered", "succeeded", "failed", "external-processing", "editing-external-processing",
                             "unconfirmed", "cancelled"],
                    "description": "Состояние заказа"
                },
                "stateTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Время изменения состояния"
                },
                "created": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата создания заказа"
                },
                "configurationType": {
                    "type": ["string", "null"],
                    "description": "Тип конфигурации"
                }
            },
            "required": ["id", "number", "addressTo", "data", "parcel", "status", "statusTime", "state", "stateTime",
                         "created", "configurationType"]

        }
    }

    order_get_by_id_or_editing = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Уникальный идентификатор заказа"
            },
            "number": {
                "type": "string",
                "description": "Номер заказа "
            },
            "addressTo": {
                "type": "object",
                "properties": {
                    "raw": {
                        "type": "string",
                        "description": "Адрес одной строкой"
                    }
                },
                "required": ["raw"]
            },
            "data": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "object",
                        "properties": {
                            "warehouse": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "Идентификатор склада"
                                    }
                                },
                                "required": ["id"]
                            },
                            "shop": {
                                "type": "object",
                                "properties": {
                                    "id": {
                                        "type": "string",
                                        "description": "Идентификатор магазина"
                                    },
                                    "number": {
                                        "type": "string",
                                        "description": "Номер магазина"
                                    },
                                    "barcode": {
                                        "type": ["string", "null"],
                                        "description": "Штрихкод магазина (может быть пустым)"
                                    }
                                },
                                "required": ["id", "number", "barcode"]
                            },
                            "payment": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["Paid", "PayOnDelivery"],
                                        "description": "Тип оплаты"
                                    },
                                    "declaredValue": {
                                        "type": "number",
                                        "description": "Объявленная стоимость"
                                    },
                                    "deliverySum": {
                                        "type": "number",
                                        "description": "Сумма доставки"
                                    }
                                },
                                "required": ["type", "declaredValue", "deliverySum"]
                            },
                            "dimension": {
                                "type": ["object", "null"],
                                "description": "Габариты",
                                "properties": {
                                    "length": {
                                        "type": "number",
                                        "description": "Длина"
                                    },
                                    "width": {
                                        "type": "number",
                                        "description": "Ширина"
                                    },
                                    "height": {
                                        "type": "number",
                                        "description": "Высота"
                                    }
                                },
                                "required": ["length", "width", "height"]
                            },
                            "weight": {
                                "type": "number",
                                "description": "Вес заказа"
                            },
                            "delivery": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["Courier", "DeliveryPoint", "PostOffice"],
                                        "description": "Тип доставки"
                                    },
                                    "service": {
                                        "type": "string",
                                        "description": "Служба доставки"
                                    },
                                    "tariff": {
                                        "type": ["string", "null"],
                                        "description": "Тариф доставки"
                                    },
                                    "deliveryPointCode": {
                                        "type": ["string", "null"],
                                        "description": "Код точки доставки"
                                    },
                                    "date": {
                                        "type": ["string", "null"],
                                        "description": "Дата доставки"
                                    },
                                    "time": {
                                        "type": ["object", "null"],
                                        "properties": {
                                            "from": {
                                                "type": ["string", "null"],
                                                "description": "Время начала доставки"
                                            },
                                            "to": {
                                                "type": ["string", "null"],
                                                "description": "Время окончания доставки"
                                            }
                                        },
                                        "description": "Время доставки"
                                    },
                                    "partner": {
                                        "type": ["string", "null"],
                                        "description": "Партнер доставки"
                                    },
                                    "intakePointCode": {
                                        "type": ["string", "null"],
                                        "description": "Код точки сдачи"
                                    }
                                },
                                "required": ["type", "service", "tariff", "deliveryPointCode", "date", "time",
                                             "partner", "intakePointCode"]
                            },
                            "recipient": {
                                "type": "object",
                                "properties": {
                                    "familyName": {
                                        "type": ["string", "null"],
                                        "description": "Фамилия"
                                    },
                                    "firstName": {
                                        "type": ["string", "null"],
                                        "description": "Имя"
                                    },
                                    "secondName": {
                                        "type": ["string", "null"],
                                        "description": "Отчество"
                                    },
                                    "fullName": {
                                        "type": ["string", "null"],
                                        "description": "Полное имя"
                                    },
                                    "phoneNumber": {
                                        "type": ["string", "null"],
                                        "description": "Номер телефона"
                                    },
                                    "email": {
                                        "type": ["string", "null"],
                                        "description": "Электронная почта"
                                    },
                                    "address": {
                                        "type": "object",
                                        "properties": {
                                            "raw": {
                                                "type": ["string", "null"],
                                                "description": "Адрес"
                                            },
                                            "countryCode": {
                                                "type": ["string", "null"],
                                                "description": "Код страны"
                                            }
                                        },
                                        "required": ["raw", "countryCode"]
                                    },
                                    "additionalPhones": {
                                        "type": "array",
                                        "items": {
                                            "type": ["string", "null"]
                                        },
                                        "description": "Дополнительные телефоны"
                                    }
                                },
                                "required": ["familyName", "firstName", "secondName", "fullName", "phoneNumber",
                                             "email", "address", "additionalPhones"]
                            },
                            "datePickup": {
                                "type": ["string", "null"],
                                "description": "Дата привоза на склад"
                            },
                            "pickupTimePeriod": {
                                "type": ["string", "null"],
                                "description": "Интервал привоза на склад"
                            },
                            "comment": {
                                "type": ["string", "null"],
                                "description": "Комментарий"
                            },
                            "places": {
                                "type": ["array", "null"],
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "items": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "article": {
                                                        "type": "string",
                                                        "description": "Артикул товара"
                                                    },
                                                    "name": {
                                                        "type": "string",
                                                        "description": "Название товара"
                                                    },
                                                    "price": {
                                                        "type": "number",
                                                        "description": "Цена товара"
                                                    },
                                                    "declaredValue": {
                                                        "type": ["number", "null"],
                                                        "description": "Объявленная стоимость товара"
                                                    },
                                                    "count": {
                                                        "type": "integer",
                                                        "description": "Количество товара"
                                                    },
                                                    "weight": {
                                                        "type": ["number", "null"],
                                                        "description": "Вес товара"
                                                    },
                                                    "vat": {
                                                        "type": "string",
                                                        "description": "НДС товара"
                                                    },
                                                    "barcode": {
                                                        "type": ["string", "null"],
                                                        "description": "Штрихкод товара"
                                                    },
                                                    "marking": {
                                                        "type": ["string", "null"],
                                                        "description": "Маркировка товара"
                                                    },
                                                    "groupMarking": {
                                                        "type": ["string", "null"],
                                                        "description": "Групповая маркировка товара"
                                                    },
                                                    "type": {
                                                        "type": ["string", "null"],
                                                        "description": "Тип товара"
                                                    },
                                                    "supplier": {
                                                        "type": ["string", "null"],
                                                        "description": "Поставщик товара"
                                                    }
                                                },
                                                "required": ["article", "name", "price", "declaredValue", "count",
                                                             "weight", "vat", "barcode", "marking", "groupMarking",
                                                             "type", "supplier"]
                                            }
                                        },
                                        "barcode": {
                                            "type": ["string", "null"],
                                            "description": "Штрихкод для места"
                                        },
                                        "shopNumber": {
                                            "type": ["string", "null"],
                                            "description": "Уникальный номер грузоместа в ИМ"
                                        },
                                        "weight": {
                                            "type": ["number", "null"],
                                            "description": "Вес места"
                                        },
                                        "dimension": {
                                            "type": ["object", "null"],
                                            "properties": {
                                                "length": {
                                                    "type": "number",
                                                    "description": "Длина места"
                                                },
                                                "width": {
                                                    "type": "number",
                                                    "description": "Ширина места"
                                                },
                                                "height": {
                                                    "type": "number",
                                                    "description": "Высота места"
                                                }
                                            },
                                            "required": ["length", "width", "height"]
                                        }
                                    },
                                    "required": ["items", "barcode", "shopNumber", "weight", "dimension"]
                                }
                            },
                            "services": {
                                "type": ["array", "null"],
                                "items": {
                                    "type": ["string", "null"]
                                },
                                "description": "Дополнительные услуги"
                            }
                        },
                        "required": ["warehouse", "shop", "payment", "dimension", "weight", "delivery", "recipient",
                                     "datePickup", "pickupTimePeriod", "comment", "places", "services"]
                    },
                    "deliveryService": {
                        "type": ["object", "null"],
                        "properties": {
                            "id": {
                                "type": ["string", "null"],
                                "description": "Идентификатор службы доставки"
                            },
                            "trackingNumber": {
                                "type": ["string", "null"],
                                "description": "Номер отслеживания"
                            },
                            "baseRate": {
                                "type": ["number", "null"],
                                "description": "Основной тариф"
                            },
                            "insrValueWithVat": {
                                "type": ["number", "null"],
                                "description": "Страховая стоимость с НДС"
                            },
                            "esppCode": {
                                "type": ["string", "null"],
                                "description": "Код ESPP"
                            },
                            "weight": {
                                "type": ["number", "null"],
                                "description": "Вес"
                            },
                            "dimensions": {
                                "type": ["object", "null"],
                                "properties": {
                                    "length": {
                                        "type": ["number", "null"],
                                        "description": "Длина"
                                    },
                                    "width": {
                                        "type": ["number", "null"],
                                        "description": "Ширина"
                                    },
                                    "height": {
                                        "type": ["number", "null"],
                                        "description": "Высота"
                                    }
                                },
                                "description": "Габариты"
                            }
                        },
                        "required": ["id", "trackingNumber", "baseRate", "insrValueWithVat", "esppCode",
                                     "weight", "dimensions"]
                    }
                },
                "required": ["request", "deliveryService"]
            },
            "parcel": {
                "type": ["object", "null"],
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Идентификатор партии"
                    }
                },
                "required": ["id"],
                "description": "Информация о партии"
            },
            "status": {
                "type": "string",
                "enum": ["created", "wait-delivery"],
                "description": "Статус заказа"
            },
            "statusTime": {
                "type": "string",
                "format": "date-time",
                "description": "Время изменения статуса"
            },
            "state": {
                "type": "string",
                "enum": ["registered", "succeeded", "failed", "external-processing", "editing-external-processing",
                         "unconfirmed", "cancelled"],
                "description": "Состояние заказа"
            },
            "stateTime": {
                "type": "string",
                "format": "date-time",
                "description": "Время изменения состояния"
            },
            "created": {
                "type": "string",
                "format": "date-time",
                "description": "Дата создания заказа"
            },
            "configurationType": {
                "type": "string",
                "enum": ["integration", "aggregation"],
                "description": "Тип конфигурации"
            }
        },
        "required": ["id", "number", "addressTo", "data", "parcel", "status", "statusTime", "state", "stateTime",
                     "created", "configurationType"]

    }

    order_get_patches = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор изменения"
                },
                "orderId": {
                    "type": "string",
                    "description": "Идентификатор заказа"
                },
                "userId": {
                    "type": "string",
                    "description": "Идентификатор пользователя"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата и время создания изменения"
                },
                "state": {
                    "type": "string",
                    "enum": ["succeeded", "failed", "external-processing"],
                    "description": "Состояние изменения"
                },
                "stateTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата и время изменения состояния"
                },
                "message": {
                    "type": ["string", "null"],
                    "description": "Сообщение к изменению"
                }
            },
            "required": ["id", "orderId", "userId", "createdAt", "state", "stateTime", "message"]
        }
    }

    order_get_statuses = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["created"],
                    "description": "Кодовое наименование статуса заказа"
                },
                "statusTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата и время установки статуса"
                }
            },
            "required": ["status", "statusTime"]
        }
    }

    order_get_details = {
        "type": "object",
        "properties": {
            "returnItems": {
                "type": ["array", "null"],
                "description": "Вложения на возврат"
            },
            "returnReason": {
                "type": ["string", "null"],
                "description": "Причина возврата заказа"
            },
            "delayReason": {
                "type": ["string", "null"],
                "description": "Причина переноса доставки"
            },
            "paymentType": {
                "type": ["string", "null"],
                "description": "Тип оплаты"
            },
            "pickupDate": {
                "type": ["string", "null"],
                "format": "date-time",
                "description": "Дата прибытия товара на склад СД"
            },
            "declaredDeliveryDate": {
                "type": ["string", "null"],
                "format": "date-time",
                "description": "Планируемая дата доставки"
            },
            "storageDateEnd": {
                "type": ["string", "null"],
                "format": "date-time",
                "description": "Срок хранения заказов"
            },
            "returnOrderTrackingNumber": {
                "type": ["string", "null"],
                "description": "Трек-номер возврата"
            }
        },
        "required": ["returnItems", "returnReason", "delayReason", "paymentType", "pickupDate", "declaredDeliveryDate",
                     "storageDateEnd", "returnOrderTrackingNumber"],
        "additionalProperties": False
    }

    order_generate_security_code = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Код выдачи"
            }
        },
        "required": ["code"]
    }
