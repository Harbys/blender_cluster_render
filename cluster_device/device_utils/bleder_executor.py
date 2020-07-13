import subprocess
import threading
import time
import unzipper
import os
import shutil
import requests


# job executor looks at queue and renders jobs in it
class Executor:
    def __init__(self, que, config):
        self.que = que
        self.config = config
        # executor is run as a separate thread
        self.run_thread = threading.Thread(target=self.thread).start()

    # called when a job is finished and sends that information to the controller
    def finish_job(self, job_id):
        data = {
            "hwid": self.config.hwid,
            "job": job_id
        }
        requests.post(f'http://{self.config.server_address}:{self.config.server_port}/dev_api', data=data)

    # removes temp files
    def cleanup(self, job_id):
        shutil.rmtree(os.path.join(self.config.tmp_path, job_id))

    # separate thread to handle the queue
    def thread(self):
        while True:
            if len(self.que.queue) == 0:
                time.sleep(1)

            else:
                # takes the first jobs
                job = self.que.queue[0]
                # unzip from network mount to temp path
                unzipper.unzip(os.path.join(self.config.nmnt, job.file_name),
                               os.path.join(self.config.tmp_path, job.job_id))
                # prepare the command for blender
                # note that for now it's prone to exploits
                command = f"{self.config.blender} -b {os.path.join(self.config.tmp_path, job.job_id, job.blend_file)}" \
                          f" -P device_utils/blender_scripts/blender_set.py -o {os.path.join(self.config.tmp_path, job.job_id, 'rendered')}" \
                          f"-s {job.fstart} -e {job.fstop} -a "
                print(f"starting render: {command}")
                # open a temporary output file to dump render info for further processing
                out = open("tmp/out", 'w+')
                # open a new subprocess for rendering and wait for completion
                blender_render = subprocess.Popen(command, shell=True, stdout=out)
                blender_render.wait()
                # get all rendered frames from temp
                rendered_files = os.listdir(os.path.join(self.config.tmp_path, job.job_id, "rendered"))
                # make a directory 'rendered' on network share if doesn't exist
                if not os.path.isdir(os.path.join(self.config.nmnt, job.file_name[:-4])):
                    os.mkdir(os.path.join(self.config.nmnt, job.file_name[:-4]))
                # copy every rendered frame to network mount
                for file in rendered_files:
                    shutil.copy(os.path.join(self.config.tmp_path, job.job_id, "rendered", file),
                                os.path.join(self.config.nmnt, job.file_name[:-4], file))
                # cleanup after the job
                self.cleanup(job.job_id)
                # finish the job
                self.finish_job(job.job_id)
                # delete job from queue
                del self.que.queue[0]
