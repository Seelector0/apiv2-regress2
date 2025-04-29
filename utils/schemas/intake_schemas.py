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
