import socket
import sys
import time
import json
import threading
from message import Message
from clientconfig import BaseConfig
# Глобальная переменная, отвечающая за остановку клиента.
shutdown = False



class ClientHandler(BaseConfig):
    """ Класс-Обработчик с бизнес-логикой клиента.
       Реализует методы получения и отображения сообщений
   """

    def __init__(self):
        super().__init__()
        # Адрес сервера (ip, port) к которому происходит подключение:
        if self.client['host'] == 'auto':
            self.client['host'] = self.get_ip()
        self.server_addr = self.get_conn('server') # Адрес сервера (ip, port) к которому происходит подключение:
        self.client_addr = self.get_conn('client') # Адрес клиента (ip, port) к которому происходит подключение:
        print(self.client_addr)
        global shutdown
        # Флаг сигнализирующий об успешном подключении
        join = False
        # Пытаемся создать соединение, если его еще нет или клиент не остановлен
        while not shutdown and not join:
            try:
                # Имя клиента в чате:
                self.name = input("Name: ").strip()
                # Создание сокета:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # Подключение сокета:
                self.socket.connect(self.client_addr)
                join = True
                # Отправка сообщения о подключении:
                connect_message = Message(
                    join=join,
                    message=f'User @{self.name} has joint to chat\n',
                    sender_name=self.name
                )
                connect_message_data = connect_message.to_json()
                self.socket.sendto(connect_message_data.encode('utf-8'),
                                   self.server_addr)
            except Exception as ex:
                print(f"ClientHandler.__init__: Что-то пошло не так: {ex}")
                shutdown = True

    @staticmethod
    def show_message(message_obj: Message):
        """
           Выводит полученное сообщение в стандартный поток вывода (консоль)
       """
        if message_obj.join:
            # Если сообщение о подключении, то выводим только его:
            sys.stdout.write(message_obj.message)
        else:
            # Иначе, добавляем имя отправителя в вывод:
            sys.stdout.write(f'@{message_obj.sender_name}: {message_obj.message}\n')

    def receive(self):
        """
           Получает сообщение из сокета и передает его в обработчик
       """
        global shutdown
        # Пока клиент не остановлен
        while not shutdown:
            try:
                # Получаем данные и адрес отправителя
                data, addr = self.socket.recvfrom(1024)
                data = dict(json.loads(data.decode('utf-8')))
                # Создаем объект сообщения из полученных данных:
                message = Message(**data)
                # Вызываем обработчик показа сообщения:
                self.show_message(message)
                time.sleep(0.2)
            except Exception as ex:
                print(f"ClientHandler.receive: Что-то пошло не так: {ex}")
                shutdown = True

    def send(self):
        """
           Принимает сообщение из потока ввода консоли,
           отправляет его в обработчик и посылает на сервер.
       """
        global shutdown
        # Пока клиент не остановлен
        while not shutdown:
            try:
                # Ожидаем ввод данных
                input_data = input("").strip()
                if input_data:
                    # Создаем объект сообщения из введенных данных:
                    message = Message(message=input_data,
                                      sender_name=self.name)
                    # Отправляем данные на сервер:
                    data = message.to_json()
                    self.socket.sendto(data.encode('utf-8'), self.server_addr)
                time.sleep(0.2)
            except Exception as ex:
                print(f"ClientHandler.send: Что-то пошло не так: {ex}")
                shutdown = True
