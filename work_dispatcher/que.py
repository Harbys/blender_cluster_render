
class Job:
    def __init__(self, job_id, filename, status='waiting'):
        self.job_id = job_id
        self.file_name = filename
        self.status = status
        self.waiting_for = []

    def add_to_waitlist(self, device_list):
        for device in device_list:
            self.waiting_for.append(device.hwid)

    def __str__(self):
        return f"job_id: {self.job_id}, file_name: {self.file_name}, status: {self.status}, waiting_for: {self.waiting_for}"


class Que:
    def __init__(self):
        self.que_list = []

    def add_job(self, job):
        self.que_list.append(job)

    def get_jobs(self):
        return self.que_list
