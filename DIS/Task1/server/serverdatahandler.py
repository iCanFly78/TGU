import socket
import sys
import time
import json
from message import Message


class ServerDataHandler:
    """Класс-Обработчик с бизнес-логикой сервера. Реализует методы обработки сообщений и их рассылки."""
    clients = {}  # Временное хранилище клиентов в виде словаря.
    # Если хотите реализовать *продвинутое решение, можете реализовать
    # взаимодействие с базой данных и сохранением пользователей.

    current_connection = None  # текущее соединение

    def _add_connection(self, name: str, addr: str):
        """ Добавляет новое соединения в словарь clients"""
        self.current_connection = addr  # адрес, с которого пришло сообщение
        self.clients[name] = addr  # добавление клиента

    def get_and_register_message(self, data: bytes, addr: str):
        """
           Сохраняет адрес запроса пользователя,
           записывается в атрибут data данные из json в виде словаря,
           добавляет имя пользователя и адрес в словарь чтобы у нас был
           доступ к адресу по имени пользователя который обратился к серверу

           :param data - полученные "сырые" данные в виде bytes
           :param addr - адрес отправителя данных
           :return Message(status_code='200', **data) - объект сообщения
       """
        data = dict(json.loads(data.decode('utf-8')))  # декодируем данные
        self._add_connection(name=data.get('sender_name',
                                           'Unknown'),
                             addr=addr)  # добавляем/обновляем список клиентов
        return Message(status_code='200', **data)

    def send_message(self, sock, message_obj: Message):
        """
           Отправляет сообщение по всем адресам в словаре
           кроме адреса отправившего запрос (эхо)
           :param sock - серверный сокет
           :param message_obj - объект сообщения
       """
        data = message_obj.to_json()  # закодированное в json сообщение
        # Отправляем сообщение всем клиентам, кроме текущего:
        for client in self.clients.values():
            if self.current_connection != client:
                sock.sendto(data.encode('utf-8'), client)
