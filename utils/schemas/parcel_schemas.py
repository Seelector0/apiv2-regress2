class ParcelSchema:
    parcels_create = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор созданного объекта"
                },
                "type": {
                    "type": "string",
                    "enum": ["Parcel"],
                    "description": "Тип созданного объекта: всегда parcel"
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
    }

    parcels_get = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Идентификатор партии"
                },
                "number": {
                    "type": "string",
                    "description": "Номер партии"
                },
                "shop": {
                    "type": ["object", "null"],
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
                            "description": "Наименование магазина"
                        },
                        "uri": {
                            "type": "string",
                            "description": "Ссылка на сайт"
                        },
                        "phone": {
                            "type": "string",
                            "description": "Номер телефона"
                        },
                        "sender": {
                            "type": "string",
                            "description": "Контактное лицо"
                        },
                        "trackingTag": {
                            "type": "string",
                            "description": "Используемое для обращения к внешнему Трекинг сервису"
                        },
                        "visibility": {
                            "type": "boolean",
                            "description": "Признак того, что магазин не удален из кабинета"
                        }
                    },
                    "required": ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"]
                },
                "deliveryServiceCode": {
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
                            "description": "Наличие агрегации"
                        }
                    },
                    "required": ["code", "name", "hasAggregation"]
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "object",
                            "properties": {
                                "orderIds": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "description": "Идентификатор заказа"
                                    },
                                    "description": "Список заказов"
                                },
                                "shipmentDate": {
                                    "type": "string",
                                    "format": "date",
                                    "description": "Дата отгрузки"
                                },
                                "printedDate": {
                                    "type": ["string", "null"],
                                    "format": "date",
                                    "description": "Дата сдачи"
                                }
                            },
                            "required": ["orderIds", "shipmentDate", "printedDate"]
                        },
                        "deliveryService": {
                            "type": "object",
                            "properties": {
                                "orders": {
                                    "type": ["array", "null"],
                                    "items": {
                                        "type": "string",
                                        "description": "Идентификатор заказа"
                                    },
                                    "description": "Список заказов для доставки"
                                },
                                "orderIds": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "description": "Идентификатор заказа"
                                    },
                                    "description": "Список идентификаторов заказов"
                                },
                                "id": {
                                    "type": "string",
                                    "description": "Идентификатор формы ф103"
                                },
                                "f103": {
                                    "type": "object",
                                    "properties": {
                                        "number": {
                                            "type": ["string", "null"],
                                            "description": "Номер f103"
                                        }
                                    }
                                }
                            },
                            "required": ["orders", "orderIds", "id"]
                        }
                    },
                    "required": ["request", "deliveryService"]
                },
                "created": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Дата создания партии"
                },
                "deleted": {
                    "type": ["string", "null"],
                    "format": "date-time",
                    "description": "Дата удаления партии"
                },
                "state": {
                    "type": "string",
                    "description": "Состояние партии"
                },
                "stateTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Время изменения состояния"
                }
            },
            "required": ["id", "number", "shop", "deliveryServiceCode", "data", "created", "deleted", "state",
                         "stateTime"]
        }
    }

    parcels_get_id_or_editing = {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Уникальный идентификатор партии"
            },
            "number": {
                "type": "string",
                "description": "Номер партии"
            },
            "shop": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Идентификатор магазина"},
                    "number": {"type": "string", "description": "Номер магазина"},
                    "name": {"type": "string", "description": "Название магазина"},
                    "uri": {"type": "string", "description": "Ссылка на сайт магазина"},
                    "phone": {"type": "string", "description": "Номер телефона магазина"},
                    "sender": {"type": "string", "description": "Контактное лицо"},
                    "trackingTag": {"type": "string", "description": "Тег трекинга"},
                    "visibility": {"type": "boolean", "description": "Отображение магазина"}
                },
                "required": ["id", "number", "name", "uri", "phone", "sender", "trackingTag", "visibility"]
            },
            "deliveryServiceCode": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Код службы доставки"},
                    "name": {"type": "string", "description": "Название службы доставки"},
                    "hasAggregation": {"type": "boolean", "description": "Признак агрегации"}
                },
                "required": ["code", "name", "hasAggregation"]
            },
            "data": {
                "type": "object",
                "properties": {
                    "request": {
                        "type": "object",
                        "properties": {
                            "orderIds": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Список идентификаторов заказов"
                            },
                            "shipmentDate": {"type": "string", "format": "date", "description": "Дата отправки"},
                            "printedDate": {"type": ["string", "null"], "description": "Дата сдачи"}
                        },
                        "required": ["orderIds", "shipmentDate", "printedDate"]
                    },
                    "deliveryService": {
                        "type": "object",
                        "properties": {
                            "orders": {"type": ["array", "null"], "items": {"type": "string"},
                                       "description": "Список заказов"},
                            "orderIds": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Список идентификаторов заказов"
                            },
                            "id": {
                                "type": "string",
                                "description": "Идентификатор формы ф103"
                            },
                            "f103": {
                                "type": "object",
                                "properties": {
                                    "number": {
                                        "type": ["string", "null"],
                                        "description": "Номер f103"
                                    }
                                }
                            }
                        },
                        "required": ["orders", "orderIds", "id"]
                    }
                },
                "required": ["request", "deliveryService"]
            },
            "created": {
                "type": "string",
                "format": "date-time",
                "description": "Дата создания"
            },
            "deleted": {"type": ["string", "null"], "description": "Дата удаления"},
            "state": {"type": "string", "description": "Состояние"},
            "stateTime": {
                "type": "string",
                "format": "date-time",
                "description": "Дата обновления состояния"
            }
        },
        "required": ["id", "number", "shop", "deliveryServiceCode", "data", "created", "deleted", "state", "stateTime"]
    }
