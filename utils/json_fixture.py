

class Body:

    @staticmethod
    def body_patch(op: str, path: str, value):
        r"""Тело для редактирования полей.
        :param op: Тип операции.
        :param path: Изменяемое поле.
        :param value: Значение.
        """
        payload = [
            {
                "op": op,
                "path": path,
                "value": value
            }
        ]
        return payload
