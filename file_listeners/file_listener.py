import os
import time
import threading
from work_dispatcher import Job
import uuid


# class used to create a separate thread for checking for file changes in listen path
# also expects a callback for function to add new jobs to queue
class FileListener:
    def __init__(self, addjob, listen_path):
        self.listenpath = listen_path
        self.last_known_files = os.listdir(self.listenpath)
        self.fthread = threading.Thread(target=self.check)
        self.fthread.start()
        self.addjob = addjob

    def get_change(self):
        files = os.listdir(self.listenpath)
        if files != self.last_known_files:
            # only gets the difference by subtracting files in directory from files last known to be in that directory
            difflist = list(set(files) - set(self.last_known_files))
            self.last_known_files = files
            ret = []
            for obj in difflist:
                # checks if is a .zip extension and not a hidden file
                if obj.split('.')[-1] == "zip" and obj[0] != '.':
                    ret.append(obj)
            if len(ret) > 0:
                return ret
            else:
                return None
        else:
            return None

    # separate thread to constantly check for changes in directory
    def check(self):
        while True:
            diff = self.get_change()
            if diff is not None:
                for obj in diff:
                    self.addjob(Job(uuid.uuid4().hex, obj))
            time.sleep(1)
