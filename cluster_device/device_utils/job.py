class Job:
    def __init__(self, job_id, file_name, main_ip, fstart, fstop):
        self.job_id = job_id
        self.file_name = file_name
        self.main_ip = main_ip
        self.fstart = fstart
        self.fstop = fstop

    def __str__(self):
        return self.job_id
