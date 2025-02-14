class ConnectionsSchema:
    connection_create = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор созданного объекта"
            },
            "type": {
                "type": "string",
                "enum": ["Delivery"],
                "description": "Тип созданного объекта: всегда Delivery"
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

    connection_get = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Код службы доставки"
                },
                "name": {
                    "type": "string",
                    "description": "Название службы доставки"
                },
                "hasAggregation": {
                    "type": "boolean",
                    "description": "Признак того, возможно ли подключить СД на агрегацию"
                },
                "id": {
                    "type": "string",
                    "description": "Идентификатор службы доставки"
                },
                "active": {
                    "type": ["boolean", "null"],
                    "description": "Признак того, что выполненная настройка активна"
                },
                "visibility": {
                    "type": ["boolean", "null"],
                    "description": "Видимость службы доставки"
                },
                "type": {
                    "type": ["string", "null"],
                    "description": "Признак того, на агрегацию или интеграцию выполнена или выполняется настройка"
                },
                "moderation": {
                    "type": "boolean",
                    "description": "Находится ли подключение на модерации"
                }
            },
            "required": ["code", "name", "hasAggregation", "id", "active", "visibility", "type", "moderation"],
            "additionalProperties": False
        }
    }

    connection_get_by_id_or_editing = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Код службы доставки"
            },
            "name": {
                "type": "string",
                "description": "Название службы доставки"
            },
            "hasAggregation": {
                "type": "boolean",
                "description": "Признак того, возможно ли подключить СД на агрегацию"
            },
            "credentials": {
                "type": "object",
                "properties": {
                    "active": {
                        "type": "boolean",
                        "description": "Признак того, что выполненная настройка активна"
                    },
                    "visibility": {
                        "type": "boolean",
                        "description": "Признак видимости аккаунта"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["integration", "aggregation"],
                                "description": "Тип интеграции"
                            }
                        },
                        "required": ["type"],
                    },
                    "settings": {
                        "type": ["array", "object"],
                        "items": {
                            "type": "object"
                        },
                        "description": "Дополнительные настройки"
                    }
                },
                "required": ["active", "visibility", "data", "settings"],
                "additionalProperties": False
            }
        },
        "required": ["code", "name", "hasAggregation", "credentials"],
        "additionalProperties": False
    }
