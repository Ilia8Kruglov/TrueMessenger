from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from os import path


folderAbs = path.dirname(path.abspath(__file__))
tmp_folder = path.join(folderAbs, 'tmp')


class FTPserver:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def run(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user("client", "12345", tmp_folder, perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((self.ip, self.port), handler)
        server.serve_forever()



