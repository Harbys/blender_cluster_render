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
from os import path


# server side definition of a file
# filename is a path to devices json config file
class Device:
    def __init__(self, ipaddr, hwid, performance, port, filename):
        self.performance = performance
        self.ipaddr = ipaddr
        self.hwid = hwid
        self.port = port
        self.filename = filename

    def __str__(self):
        return self.hwid

    # saves devices data to json file
    def save(self):
        data = {
            "ip": self.ipaddr,
            "hwid": self.hwid,
            "performance": self.performance,
            "port": self.port
        }
        with open(f"devices/{self.filename}", "w") as self_datafile:
            json.dump(data, self_datafile, indent=2)

    # returns a sorted list od device performances
    @staticmethod
    def performance_list(devices):
        ret = []
        for dev in devices:
            ret.append(dev.performance)
        ret.sort()
        return ret

    # sends information to a device about a job, to then be executed by the device
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
        ret = json.loads(requests.post(f'http://{self.ipaddr}:{self.port}/add_to_work_que', json=json_data).content.decode("utf-8"))
        if ret["action"] == "job_added":
            return True
        else:
            return False


# cluster controller
class Cluster:
    def __init__(self, config):
        # devices is a list of devices sorted by their performance
        self.devices = self.sort_devices_by_perf(self.create_devices_list())
        self.queue = work_dispatcher.Que()
        self.file_listener = file_listeners.FileListener(self.queue.add_job, config.listen_path)
        # config is passed from web dashboard
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
            # goes over every job in queue and checks if it has been previously handled
            for job in self.queue.get_jobs():
                if job.status == 'waiting':
                    unzip(path.join(self.config.listen_path, job.file_name), path.join(self.config.tmp_path, job.job_id))
                    # create full path to blender file
                    blend_file_path = path.join(path.join(self.config.tmp_path, job.job_id), self.find_blender_file(path.join(self.config.tmp_path, job.job_id)))
                    # send information to every device to pull the data and start rendering
                    self.dispatch_work(blend_file_path, job.job_id, job.file_name, self.find_blender_file(path.join(self.config.tmp_path, job.job_id)))
                    # jobs waiting list is set to every device, and change jobs status
                    job.add_to_waitlist(self.devices)
                    job.status = 'pending'
                    # prints job for debug purposes
                    print(job)
            time.sleep(1)

    def dispatch_work(self, blend_file, job_id, file_name, blend_file_name):
        # gets starting frame number, end frame number and total number of frames
        ftsart, fstop, total = get_frames_info(blend_file)
        # passes total amount of frames to be split between all devices and gets an array with number of frames to be
        # rendered by devices
        divided_array = self.divide_alg(total)
        frame = ftsart
        for device in self.devices:
            # dispatches work with job id, starting frame, ending frame (last sent frame + number from divided array)
            device.dispatch_job(job_id, frame, frame+divided_array[self.devices.index(device)] - 1, file_name, blend_file_name)
            frame += frame+divided_array[self.devices.index(device)] - 1

    # looks for a file with .blend extension
    @staticmethod
    def find_blender_file(path):
        listed = listdir(path)
        for obj in listed:
            if obj.split('.')[-1] == "blend":
                return obj
        return None

    # algorithm for dividing work between devices based on their performance numbers
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

    # gets every .json file in devices folder
    @staticmethod
    def get_device_files():
        read_list = listdir('devices/')
        device_list = []
        for obj in read_list:
            if obj.split('.')[-1] == "json":
                device_list.append(obj)
        return device_list

    # creates list filled with Device class instances
    def create_devices_list(self):
        name_list = self.get_device_files()
        device_list = []
        for name in name_list:
            with open(f'devices/{name}', 'r') as f:
                jp = json.load(f)
                device_list.append(Device(jp['ip'], jp['hwid'], jp['performance'], jp['port'], name))
        return device_list

    # deletes id from jobs waiting list and check for completed jobs
    def delete_waiting_for(self, job_id, hwid):
        self.queue.del_from_waiting(job_id, hwid)
        empty = self.queue.get_empty()
        # delete every temp folder
        for empty_job_id in empty:
            shutil.rmtree(f"{self.config.tmp_path}{empty_job_id}")

    def find_device_by_hwid(self, hwid):
        for device in self.devices:
            if device.hwid == hwid:
                return device
        raise KeyError

    def edit_device(self, data):
        # edits device with provided data
        for i, device in enumerate(self.devices):
            if device.hwid == data["hwid_old"]:
                self.devices[i].hwid = data["hwid"]
                self.devices[i].ipaddr = data["ip_addr"]
                self.devices[i].performance = int(data["performance"])
                self.devices[i].port = data["port"]
                self.devices[i].save()

                self.devices = self.sort_devices_by_perf(self.devices)
                break

