class WarehousesSchema:
    warehouses_create = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор созданного объекта"
            },
            "type": {
                "type": "string",
                "enum": ["Warehouse"],
                "description": "Тип созданного объекта: всегда Warehouse"
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

    warehouses_get = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор склада"
                },
                "number": {
                    "type": "string",
                    "description": "Номер склада"
                },
                "name": {
                    "type": "string",
                    "description": "Название склада"
                },
                "visibility": {
                    "type": "boolean",
                    "description": "Признак того, что склад не удален из кабинета"
                },
                "address": {
                    "type": "object",
                    "properties": {
                        "raw": {
                            "type": "string",
                            "description": "Адрес склада"
                        },
                    },
                    "required": ["raw"],
                    "description": "Адрес склада"
                },
                "contact": {
                    "type": ["object", "null"],
                    "properties": {
                        "fullName": {
                            "type": "string",
                            "description": "Полное имя контактного лица"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Телефон контактного лица"
                        },
                        "email": {
                            "type": ["string", "null"],
                            "description": "Email контактного лица"
                        }
                    },
                    "description": "Контактные данные склада"
                },
                "workingTime": {
                    "type": ["object", "null"],
                    "description": "Рабочее время склада"
                },
                "pickup": {
                    "type": ["boolean", "null"],
                    "description": "Признак доступности для самовывоза"
                },
                "dpdPickupNum": {
                    "type": ["string", "null"],
                    "description": "Номер регулярного заказа DPD"
                },
                "lPostWarehouseId": {
                    "type": ["string", "null"],
                    "description": "Идентификатора склада партнера Л-Пост"
                },
                "yandexWarehouseId": {
                    "type": ["string", "null"],
                    "description": "Идентификатор склада партнера Яндекса"
                },
                "comment": {
                    "type": ["string", "null"],
                    "description": "Комментарий к складу"
                },
            },
            "required": ["id", "number", "name", "visibility", "address", "contact", "workingTime", "pickup",
                         "dpdPickupNum", "lPostWarehouseId", "yandexWarehouseId", "comment"]
        }
    }

    warehouses_get_by_id_or_editing = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Идентификатор склада"
            },
            "number": {
                "type": "string",
                "description": "Номер склада"
            },
            "name": {
                "type": "string",
                "description": "Название склада"
            },
            "visibility": {
                "type": "boolean",
                "description": "Признак того, что склад не удален из кабинета"
            },
            "address": {
                "type": "object",
                "properties": {
                    "raw": {
                        "type": "string",
                        "description": "Адрес склада"
                    },
                },
                "required": ["raw"],
                "description": "Адрес склада"
            },
            "contact": {
                "type": ["object", "null"],
                "properties": {
                    "fullName": {
                        "type": "string",
                        "description": "Полное имя контактного лица"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Телефон контактного лица"
                    },
                    "email": {
                        "type": ["string", "null"],
                        "description": "Email контактного лица"
                    }
                },
                "description": "Контактные данные склада"
            },
            "workingTime": {
                "type": ["object", "null"],
                "description": "Рабочее время склада"
            },
            "pickup": {
                "type": ["boolean", "null"],
                "description": "Признак доступности для самовывоза"
            },
            "dpdPickupNum": {
                "type": ["string", "null"],
                "description": "Номер регулярного заказа DPD"
            },
            "lPostWarehouseId": {
                "type": ["string", "null"],
                "description": "Идентификатора склада партнера Л-Пост"
            },
            "yandexWarehouseId": {
                "type": ["string", "null"],
                "description": "Идентификатор склада партнера Яндекса"
            },
            "comment": {
                "type": ["string", "null"],
                "description": "Комментарий к складу"
            },
        },
        "required": ["id", "number", "name", "visibility", "address", "contact", "workingTime", "pickup",
                     "dpdPickupNum", "lPostWarehouseId", "yandexWarehouseId", "comment"]
    }
