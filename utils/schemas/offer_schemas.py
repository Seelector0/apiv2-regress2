class OfferSchema:
    offer_get = {
        "type": "object",
        "properties": {
            "Courier": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/deliveryObject"
                }
            },
            "DeliveryPoint": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/deliveryObject"
                }
            },
            "PostOffice": {
                "type": "array",
                "items": {
                    "$ref": "#/definitions/deliveryObject"
                }
            }
        },
        "minProperties": 1,
        "additionalProperties": False,
        "definitions": {
            "deliveryObject": {
                "type": "object",
                "properties": {
                    "delivery": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "enum": ["RussianPost", "RussianPostMarketPlace", "TopDelivery", "Cdek", "Boxberry",
                                         "Dpd", "Cse", "FivePost", "YandexGo", "YandexDelivery", "DostavkaClub",
                                         "Dalli", "LPost", "Halva", "Pecom", "PonyExpress", "AlemTat", "KazPost",
                                         "MetaShip"],
                                "description": "Код службы доставки"
                            },
                            "name": {
                                "type": "string",
                                "description": "Название службы доставки"
                            }
                        },
                        "required": ["code", "name"],
                        "description": "Информация о службе доставки"
                    },
                    "service": {
                        "type": "object",
                        "properties": {
                            "base": {
                                "type": ["string", "null"],
                                "description": "Базовая стоимость доставки в рублях."
                            },
                            "service": {
                                "type": ["string", "null"],
                                "description": "Стоимость дополнительных услуг."
                            },
                            "total": {
                                "type": "string",
                                "description": "Общая стоимость доставки (с учетом всех услуг и сборов)."
                            },
                            "declaredValue": {
                                "type": ["string", "null"],
                                "description": "Заявленная стоимость товара."
                            },
                            "baseWithoutVat": {
                                "type": ["string", "null"],
                                "description": "Базовая стоимость доставки без НДС."
                            },
                            "totalWithoutVat": {
                                "type": ["string", "null"],
                                "description": "Общая стоимость доставки без НДС."
                            },
                            "serviceWithoutVat": {
                                "type": ["string", "null"],
                                "description": "Стоимость дополнительных услуг без НДС."
                            },
                            "declaredValueWithoutVat": {
                                "type": ["string", "null"],
                                "description": "Заявленная стоимость товара без НДС."
                            }
                        },
                        "required": ["base", "service", "total", "declaredValue", "baseWithoutVat", "totalWithoutVat",
                                     "serviceWithoutVat", "declaredValueWithoutVat"],
                        "description": "Информация о стоимости доставки и дополнительных услуг"
                    },
                    "tariff": {
                        "type": ["object", "null"],
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Идентификатор тарифа."
                            },
                            "name": {
                                "type": "string",
                                "description": "Название тарифа."
                            }
                        },
                        "required": ["id", "name"],
                        "description": "Информация о тарифе."
                    },
                    "type": {
                        "type": "string",
                        "enum": ["Courier", "PostOffice", "DeliveryPoint"],
                        "description": "Тип доставки."
                    },
                    "daysMin": {
                        "type": ["number", "null"],
                        "description": "Минимальное количество дней доставки."
                    },
                    "daysMax": {
                        "type": ["number", "null"],
                        "description": "Максимальное количество дней доставки."
                    },
                    "errors": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Список ошибок, связанных с доставкой."
                    },
                    "additionalInfo": {
                        "type": ["array", "null"],
                        "description": "Дополнительная информация о доставке."
                    }
                },
                "required": ["delivery", "service", "tariff", "type", "daysMin", "daysMax", "errors", "additionalInfo"],
            }
        }
    }
