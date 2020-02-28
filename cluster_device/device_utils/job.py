class Job:
    def __init__(self, job_id, file_name, fstart, fstop, blend_file):
        self.job_id = job_id
        self.file_name = file_name
        self.fstart = fstart
        self.fstop = fstop
        self.blend_file = blend_file

    def __str__(self):
        return self.job_id
