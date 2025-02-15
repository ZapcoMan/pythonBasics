import threading

from 网络安全.wifi.crackingPassword import 破解密码


class MyThread(threading.Thread):
    def __init__(self, arg):
        super(MyThread, self).__init__()
        self.arg = arg

    def run(self):
        破解密码(str(self.arg), self.arg)
