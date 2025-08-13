class IntakeSchema:
    intake_create = {
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
                "enum": [201],
                "description": "HTTP-статус ответа"
            }
        },
        "required": ["id", "type", "url", "status"],
        "additionalProperties": False
    }

    intake_get_by_id_or_patch = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Идентификатор объекта"},
            "number": {"type": "string", "description": "Номер объекта"},
            "deliveryServiceId": {"type": ["string", "null"], "description": "ID службы доставки или null"},
            "status": {"type": "string", "description": "Статус объекта"},
            "message": {"type": ["string", "null"], "description": "Сообщение или null"},
            "createdAt": {"type": "string", "format": "date", "description": "Дата создания объекта"},
            "request": {
                "type": "object",
                "properties": {
                    "deliveryService": {"type": "string", "description": "Служба доставки"},
                    "from": {
                        "type": "object",
                        "properties": {
                            "warehouseId": {"type": "string", "description": "ID склада отправки"}
                        },
                        "required": ["warehouseId"],
                        "additionalProperties": False
                    },
                    "to": {
                        "type": "object",
                        "properties": {
                            "warehouseId": {"type": "string", "description": "ID склада назначения"}
                        },
                        "required": ["warehouseId"],
                        "additionalProperties": False
                    },
                    "dimension": {
                        "type": "object",
                        "properties": {
                            "length": {"type": "number"},
                            "width": {"type": "number"},
                            "height": {"type": "number"}
                        },
                        "required": ["length", "width", "height"],
                        "additionalProperties": False
                    },
                    "weight": {"type": "number", "description": "Вес груза"},
                    "countCargoPlace": {"type": "integer", "description": "Количество мест груза"},
                    "date": {"type": "string", "format": "date", "description": "Дата забора груза"},
                    "shop": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "ID магазина"},
                            "number": {"type": "string", "description": "Номер магазина"}
                        },
                        "required": ["id", "number"],
                        "additionalProperties": False
                    },
                    "time": {
                        "type": "object",
                        "properties": {
                            "from": {"type": "string", "description": "Время с"},
                            "to": {"type": "string", "description": "Время до"}
                        },
                        "required": ["from", "to"],
                        "additionalProperties": False
                    },
                    "contact": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "Имя контакта"},
                            "phone": {"type": "string", "description": "Телефон контакта"}
                        },
                        "required": ["name", "phone"],
                        "additionalProperties": False
                    },
                    "comment": {"type": ["string", "null"], "description": "Комментарий"},
                    "description": {"type": "string", "description": "Описание груза"},
                    "services": {"type": ["array", "null"], "description": "Дополнительные услуги или null"}
                },
                "required": ["deliveryService", "from", "to", "dimension", "weight", "countCargoPlace", "date", "shop",
                             "time", "contact", "description"],
                "additionalProperties": False
            }
        },
        "required": ["id", "number", "deliveryServiceId", "status", "message", "createdAt", "request"],
        "additionalProperties": False
    }

    intake_time_schedules = {
        "type": "object",
        "properties": {
            "schedule": {
                "type": "string",
                "enum": ["intervals"],
                "description": "Тип расписания"
            },
            "intervals": {
                "type": "array",
                "description": "Список доступных интервалов для забора",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {
                            "type": "string",
                            "pattern": "^\\d{2}:\\d{2}$",
                            "description": "Время начала интервала (формат HH:MM)"
                        },
                        "to": {
                            "type": "string",
                            "pattern": "^\\d{2}:\\d{2}$",
                            "description": "Время окончания интервала (формат HH:MM)"
                        },
                        "date": {
                            "type": "string",
                            "format": "date",
                            "description": "Дата, на которую действует интервал"
                        },
                        "externalTimeIntervalId": {
                            "type": "string",
                            "description": "Внешний идентификатор интервала"
                        }
                    },
                    "required": ["from", "to", "date", "externalTimeIntervalId"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["schedule", "intervals"],
        "additionalProperties": False
    }
