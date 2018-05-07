import json
import re
from PyQt5.QtCore import QObject, pyqtSignal


class BaseReceiver:
    gotData = pyqtSignal(str)

    def __init__(self, client, request_queue):
        self.request_queue = request_queue
        self.sock = client.tcp_socket
        self.client = client
        self.connected = False

    def get_message(self):
        self.connected = True
        while self.connected:
            if not self.connected:
                break
            try:
                message = self.client.receive_message()
                for m in [json.loads(i) for i in re.findall(r'{[^{}]*}', message)]:
                    self.request_queue.put(m)
                    while not self.request_queue.empty():
                        msg = self.request_queue.get()
                        if msg['action'] == 'msg':
                            text_msg = "[{}] {}:   {}".format(msg.get('time'), msg.get('from'), msg.get('message'))
                            self.gotData.emit(text_msg)
            except Exception as e:
                print(e)


class GuiListener(BaseReceiver, QObject):
    gotData = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, client, request_queue):
        BaseReceiver.__init__(self, client, request_queue)
        QObject.__init__(self)

    def get_message(self):
        super().get_message()
        self.finished.emit(0)








