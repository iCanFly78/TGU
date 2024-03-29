import threading
from clienthandler import ClientHandler

if __name__ == '__main__':
    # Создаем обработчик клиента
    handler = ClientHandler()
    # В отдельном потоке вызываем обработку получения сообщений:
    recv_thread = threading.Thread(target=handler.receive)
    recv_thread.start()
    # В главном потоке вызываем обработку отправки сообщений:
    handler.send()
    # Прикрепляем поток с обработкой получения сообщений к главному потоку:
    recv_thread.join()
