from ftplib import FTP
from os import path
import os


folderAbs = path.dirname(path.abspath(__file__))

class FTPclient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.ftp = FTP('', timeout=2)

    def run(self):
        self.ftp.connect(self.ip, self.port)
        self.ftp.login(user='client', passwd='12345')
        self.ftp.retrlines('LIST')
        self.ftp.cwd('')

    def uploadFile(self, path, name):
        try:
            filename = '{}.png'.format(name)
            self.run()
            self.ftp.storbinary('STOR ' + filename, open(path, 'rb'))
            self.ftp.quit()
        except:
            pass

    def downloadFile(self, name):
        try:
            filename = '{}.png'.format(name)
            imgPath = path.join(folderAbs, 'avatars/')
            os.chdir(imgPath)
            self.run()
            localfile = open(filename, 'wb')
            self.ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
            self.ftp.quit()
            localfile.close()
            return imgPath + filename
        except:
            return False


if __name__ == "__main__":
    ftp = FTPclient("127.0.0.1", 1026)
    # ftp.uploadFile('/Users/semeandr/PycharmProjects/Messanger/ClientRepo/avatars/default_profile.png', 'default_profile.png')
    ftp.downloadFile('Alesya')