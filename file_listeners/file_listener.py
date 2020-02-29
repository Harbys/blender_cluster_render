import os
import time
import threading
from work_dispatcher import Job
import uuid


class FileListener:
    def __init__(self, addjob, listen_path):
        self.listenpath = listen_path
        self.last_known_files = os.listdir(self.listenpath)
        self.fthread = threading.Thread(target=self.check)
        self.fthread.start()
        self.que = addjob

    def get_change(self):
        files = os.listdir(self.listenpath)
        if files != self.last_known_files:
            difflist = list(set(files) - set(self.last_known_files))
            self.last_known_files = files
            ret = []
            for obj in difflist:
                if obj.split('.')[-1] == "zip" and obj[0] != '.':
                    ret.append(obj)
            if len(ret) > 0:
                return ret
            else:
                return None
        else:
            return None

    def check(self):
        while True:
            diff = self.get_change()
            if diff is not None:
                for obj in diff:
                    self.que(Job(uuid.uuid4().hex, obj))
            time.sleep(1)
