class WebhookSchema:
    webhook_create_or_get_by_id = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор веб-хука"
            },
            "shopId": {
                "type": "string",
                "description": "Идентификатор магазина"
            },
            "url": {
                "type": "string",
                "format": "uri",
                "description": "URL для получения данных"
            },
            "name": {
                "type": "string",
                "description": "Наименование веб-хука"
            },
            "secret": {
                "type": "string",
                "description": "Секретный ключ для подписки"
            },
            "eventType": {
                "type": "string",
                "enum": ["StatusUpdate", "AcceptanceRequested"],
                "description": "Тип события"
            },
            "active": {
                "type": "boolean",
                "description": "Является ли веб-хук активным"
            },
            "createdAt": {
                "type": "string",
                "format": "date-time",
                "description": "Дата создания"
            },
            "updatedAt": {
                "type": "string",
                "format": "date-time",
                "description": "Дата последнего обновления"
            }
        },
        "required": ["id", "shopId", "url", "name", "eventType", "active", "createdAt", "updatedAt"],
        "additionalProperties": False
    }

    webhook_get = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор веб-хука"
                },
                "shopId": {
                    "type": "string",
                    "description": "Идентификатор магазина"
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "description": "URL для получения данных"
                },
                "name": {
                    "type": "string",
                    "description": "Наименование веб-хука"
                },
                "secret": {
                    "type": "string",
                    "description": "Секретный ключ для подписки"
                },
                "eventType": {
                    "type": "string",
                    "enum": ["StatusUpdate", "AcceptanceRequested"],
                    "description": "Тип события"
                },
                "active": {
                    "type": "boolean",
                    "description": "Является ли веб-хук активным"
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата создания"
                },
                "updatedAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата последнего обновления"
                }
            },
            "required": ["id", "shopId", "url", "name", "eventType", "active", "createdAt", "updatedAt"],
            "additionalProperties": False
        }
    }
