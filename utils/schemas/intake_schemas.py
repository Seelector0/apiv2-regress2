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
                "description": "HTTP-статус ответа"
            }
        },
        "required": ["id", "type", "url", "status"],
        "additionalProperties": False
    }
