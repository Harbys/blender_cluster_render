from os import listdir
import file_listeners
import requests
import work_dispatcher
from blender_render_info import get_frames_info
from unzipper import unzip
import threading
import time
import json
import shutil


class Device:
    def __init__(self, ipaddr, hwid, performance, port):
        self.performance = performance
        self.ipaddr = ipaddr
        self.hwid = hwid
        self.port = port

    @staticmethod
    def performance_list(devices):
        ret = []
        for dev in devices:
            ret.append(dev.performance)
        ret.sort()
        return ret

    def dispatch_job(self, job_id, fstart, fend, file_name, blend_file):
        pass
        data = {
            "job_id": job_id,
            "fstart": fstart,
            "fend": fend,
            "file_name": file_name,
            "blend_file": blend_file
        }
        json_data = json.dumps(data)
        ret = json.loads(requests.post(f'http://{self.ipaddr}:2540/add_to_work_que', json=json_data).content.decode("utf-8"))
        if ret["action"] == "job_added":
            return True
        else:
            return False


class Cluster:
    def __init__(self, config):
        self.devices = self.sort_devices_by_perf(self.create_devices_list())
        self.queue = work_dispatcher.Que()
        self.file_listener = file_listeners.FileListener(self.queue.add_job, config.listen_path)
        self.config = config
        self.que_listener_thread = threading.Thread(target=self.que_listener).start()

    @staticmethod
    def sort_devices_by_perf(devices):
        sorted_list = []
        for device in devices:
            if len(sorted_list) == 0:
                sorted_list.append(device)
                continue
            index = 0
            for sub_device in sorted_list:
                if device.performance > sub_device.performance:
                    index += 1
                else:
                    break
            sorted_list.insert(index, device)
        return sorted_list

    def que_listener(self):
        while True:
            for job in self.queue.get_jobs():
                if job.status == 'waiting':
                    unzip(self.config.listen_path+job.file_name, self.config.tmp_path+job.job_id)
                    print(self.config.listen_path+job.file_name)
                    blend_file_path = f'{self.config.tmp_path+job.job_id}/{self.find_blender_file(self.config.tmp_path+job.job_id)}'
                    self.dispatch_work(blend_file_path, job.job_id, job.file_name, self.find_blender_file(self.config.tmp_path+job.job_id))
                    job.add_to_waitlist(self.devices)
                    job.status = 'pending'
                    print(job)
            time.sleep(1)

    def dispatch_work(self, blend_file, job_id, file_name, blend_file_name):
        ftsart, fstop, total = get_frames_info(blend_file)
        divided_array = self.divide_alg(total)
        frame = ftsart
        for device in self.devices:
            device.dispatch_job(job_id, frame, frame+divided_array[self.devices.index(device)] - 1, file_name, blend_file_name)
            frame += frame+divided_array[self.devices.index(device)] - 1

    @staticmethod
    def find_blender_file(path):
        listed = listdir(path)
        for obj in listed:
            if obj.split('.')[-1] == "blend":
                return obj
        return None

    def divide_alg(self, totalframes):
        perflist = Device.performance_list(self.devices)
        base_divide = []
        base = totalframes // sum(perflist)
        for val in perflist:
            base_divide.append(val * base)
        rest1 = totalframes - sum(base_divide)
        nth_loop = 0
        counter = 0
        for fake_index in range(rest1):
            actual_index = ((fake_index * -1) - 1) + (nth_loop * len(base_divide))
            base_divide[actual_index] += 1
            counter += 1
            if counter == len(base_divide):
                counter = 0
                nth_loop += 1
        return base_divide

    @staticmethod
    def get_device_files():
        read_list = listdir('devices/')
        device_list = []
        for obj in read_list:
            if obj.split('.')[-1] == "json":
                device_list.append(obj)
        return device_list

    def create_devices_list(self):
        name_list = self.get_device_files()
        device_list = []
        for name in name_list:
            with open(f'devices/{name}', 'r') as f:
                jp = json.load(f)
                device_list.append(Device(jp['ip'], jp['hwid'], jp['performance'], jp['port']))
        return device_list

    def delete_waiting_for(self, job_id, hwid):
        self.queue.del_from_waiting(job_id, hwid)
        empty = self.queue.get_empty()
        for empty_job_id in empty:
            shutil.rmtree(f"{self.config.tmp_path}{empty_job_id}")
