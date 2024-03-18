import socket
import sys
import time
import json
import threading


class Message:
    """Класс-Сообщение. Представляет сообщения, которые будут приходить от клиентов."""

    def __init__(self, **data):
        # Устанавливаем дополнительные атрибуты сообщения.
        self.status = 'online'
        if 'join' not in data:
            self.join = False

        # Распаковываем кортеж именованных аргументов в параметры класса.
        # Паттерн Builder
        for param, value in data.items():
            setattr(self, param, value)

        # время получения сообщения:
        self.curr_time = time.strftime("%Y-%m-%d-%H.%M.%S",
                                       time.localtime())

    def to_json(self):
        """Возвращает атрибуты класса и их значения в виде json.
           Использует стандартный модуль python - json.
       """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)
