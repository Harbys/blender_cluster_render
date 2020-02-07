import os
import time
from subprocess import run as run_command
import threading


class FileListener:
    def __init__(self):
        self.savepath = '/Users/harbys/Desktop/'
        self.listenpath = '/Users/harbys/Desktop/to_render/'
        self.last_known_files = os.listdir(self.listenpath)
        self.fthread = threading.Thread(target=self.check)
        self.fthread.start()

    def get_change(self):
        files = os.listdir(self.listenpath)
        if files != self.last_known_files:
            difflist = list(set(files) - set(self.last_known_files))
            self.last_known_files = files
            ret = []
            for obj in difflist:
                if obj.split('.')[-1] == "zip":
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
                    code = run_command(
                        ["/Applications/Blender.app/Contents/MacOS/Blender", "-b", self.listenpath + obj, "-o",
                         self.savepath + f'render_{obj.split(".")[0]}/', '-a']).returncode
            time.sleep(5)
