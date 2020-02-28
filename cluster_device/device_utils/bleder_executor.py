import subprocess
import threading
import time
import unzipper


class Executor:
    def __init__(self, que, config):
        self.que = que
        self.config = config
        self.run_thread = threading.Thread(target=self.thread).start()

    def thread(self):
        while True:
            if len(self.que.queue) == 0:
                time.sleep(1)

            else:
                job = self.que.queue[0]
                unzipper.unzip(f'{self.config.nmnt}{job.file_name}', f"{self.config.tmp_path}{job.job_id}")
                command = f"{self.config.blender} -b {self.config.tmp_path}{job.job_id}/{job.blend_file} -P device_utils/blender_scripts/blender_set.py -o {self.config.tmp_path}{job.job_id}/rendered/ -s {job.fstart} -e {job.fstop} -a"
                print(f"starting render: {command}")
                out = open("tmp/out", 'w+')
                blender_render = subprocess.Popen(command, shell=True, stdout=out)
                blender_render.wait()
                del self.que.queue[0]
