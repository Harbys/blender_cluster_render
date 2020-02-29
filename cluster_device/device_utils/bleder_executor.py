import subprocess
import threading
import time
import unzipper
import os
import shutil
import requests


class Executor:
    def __init__(self, que, config):
        self.que = que
        self.config = config
        self.run_thread = threading.Thread(target=self.thread).start()

    def finish_job(self, job_id):
        data = {
            "hwid": self.config.hwid,
            "job": job_id
        }
        requests.post(f'http://{self.config.server_address}:{self.config.server_port}/dev_api', data=data)

    def cleanup(self, job_id):
        shutil.rmtree(f"{self.config.tmp_path}{job_id}")

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
                src_files = os.listdir(self.config.tmp_path+job.job_id+"/rendered/")
                if not os.path.isdir(self.config.nmnt+job.file_name[:-4]):
                    os.mkdir(self.config.nmnt+job.file_name[:-4])
                for file in src_files:
                    shutil.copy(self.config.tmp_path+job.job_id+f"/rendered/{file}", self.config.nmnt+job.file_name[:-4]+f"/{file}")
                self.cleanup(job.job_id)
                self.finish_job(job.job_id)
                del self.que.queue[0]
