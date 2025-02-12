class ShopSchema:
    shop_create = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор созданного объекта"
            },
            "type": {
                "type": "string",
                "enum": ["Shop"],
                "description": "Тип созданного объекта: всегда Shop"
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

    shop_get = {
        "type": "array",
        "items": {
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
                "name": {
                    "type": "string",
                    "description": "Название магазина"
                },
                "uri": {
                    "type": "string",
                    "format": "uri",
                    "description": "Ссылка на сайт"
                },
                "phone": {
                    "type": ["string", "null"],
                    "description": "Телефон магазина"
                },
                "sender": {
                    "type": ["string", "null"],
                    "description": "Контактное лицо"
                },
                "trackingTag": {
                    "type": "string",
                    "description": "Сервисное поле, используемое для обращения к внешнему Трекинг сервису"
                },
                "visibility": {
                    "type": "boolean",
                    "description": "Статус видимости магазина"
                }
            },
            "required": ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"],
            "additionalProperties": False
        }
    }

    shop_get_by_id_or_editing = {
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
            "name": {
                "type": "string",
                "description": "Название магазина"
            },
            "uri": {
                "type": "string",
                "format": "uri",
                "description": "Ссылка на сайт"
            },
            "phone": {
                "type": ["string", "null"],
                "description": "Телефон магазина"
            },
            "sender": {
                "type": ["string", "null"],
                "description": "Контактное лицо"
            },
            "trackingTag": {
                "type": "string",
                "description": "Сервисное поле, используемое для обращения к внешнему Трекинг сервису"
            },
            "visibility": {
                "type": "boolean",
                "description": "Статус видимости магазина"
            }
        },
        "required": ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"],
        "additionalProperties": False
    }
