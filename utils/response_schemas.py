class SchemaInfo:
    create_order = {
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

    get_order_by_id = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "number": {"type": "string"},
            "addressTo": {
                "type": "object",
                "properties": {
                    "raw": {"type": "string"}
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
                                    "id": {"type": "string"}
                                },
                                "required": ["id"]
                            }
                        },
                        "required": ["warehouse"]
                    }
                },
                "required": ["request"]
            },
            "parcel": {"type": ["object", "null"]},  # Может быть объектом или null
            "status": {"type": "string"},
            "statusTime": {"type": "string"},
            "statusReason": {"type": ["string", "null"]},  # Может быть строкой или null
            "state": {"type": "string"},
            "stateTime": {"type": "string"},
            "stateMessage": {"type": ["string", "null"]},  # Может быть строкой или null
            "created": {"type": "string"},
            "configurationType": {"type": "string"}
        },
        "required": [
            "id", "number", "addressTo", "data", "status", "statusTime", "state", "stateTime", "created",
            "configurationType"
        ]
    }

    get_order_details = {
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
            }
        },
        "required": [
            "returnItems",
            "returnReason",
            "delayReason",
            "paymentType",
            "pickupDate",
            "declaredDeliveryDate",
            "storageDateEnd"
        ],
        "additionalProperties": False
    }

    create_order_from_file = {
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

    create_intake = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор созданного объекта"
            },
            "type": {
                "type": "string",
                "enum": ["Intake"],
                "description": "Тип созданного объекта: всегда Intake"
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


SCHEMAS = SchemaInfo()
