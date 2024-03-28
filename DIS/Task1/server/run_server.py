import socket
import sys
# import logging
from serverdatahandler import ServerDataHandler

# logging.basicConfig(filename='log.txt', filemode='a', level=logging.INFO,
#                     format="%(asctime)s(%(levelname)s): %(message)s")

# logging.info(f'Running server')

if __name__ == "__main__":
    # Создаем объект серверного сокета.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # host и port на котором будет запущен сервер
    host = 'localhost'
    port = 8888
    # Устанавливаем опцию для текущего адреса сокета,
    # чтобы его можно было переиспользовать в последующих перезапуска:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Регистрируем сокет
    s.bind((host, port))
    # Создаем обработчик бизнес-логики
    data_handler = ServerDataHandler()
    # Флаг для остановки работы сервера
    quit_server = False
    print("Server started")

    # Основной цикл работы сервера.
    while not quit_server:
        try:
            # Получаем данные из буфера сокета
            recv_data, recv_addr = s.recvfrom(1024)
            # Логируем информацию в консоль
            sys.stdout.write(recv_data.decode('utf-8'))

            # Регистрируем сообщение
            message = data_handler.get_and_register_message(recv_data,
                                                            recv_addr)
            # Посылаем сообщение в чат (эхо)
            data_handler.send_message(s, message)

        except Exception as ex:
            # Если произошла ошибка, останавливаем работу сервера.
            print(f"Server stopped, because {ex}")
            quit_server = True
    # Закрываем серверное соединение.
    s.close()
