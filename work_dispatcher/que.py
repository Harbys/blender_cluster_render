# Contains server side definition of a job to be done
class Job:
    def __init__(self, job_id, filename, status='waiting'):
        # job id is given while creating the job and is a random uuid
        self.job_id = job_id
        # file name this job operatees on
        self.file_name = filename
        # status is supposed to represent current completion level, not fully implemented yet
        self.status = status
        # this is a list of device ids that execute a part of this job, only when this is empty the job is considered
        # finished
        self.waiting_for = []

    # adds device ids to the wait list, expects a list of device objects
    def add_to_waitlist(self, device_list):
        for device in device_list:
            self.waiting_for.append(device.hwid)

    # definition for stringifying this job, used mainly for debugging
    def __str__(self):
        return f"job_id: {self.job_id}, file_name: {self.file_name}, status: {self.status}, waiting_for: {self.waiting_for}"

    # deletes id from wait list
    def del_from_waiting(self, hwid):
        self.waiting_for.remove(hwid)


# server side definition for queue of jobs
class Que:
    def __init__(self):
        # list of currently executed jobs
        self.que_list = []

    # simply adds a new job to the list
    def add_job(self, job):
        self.que_list.append(job)

    # returns all jobs as a list
    def get_jobs(self):
        return self.que_list

    # deletes specified id from a job in the list, expects jobs id and device id
    # returns False if there was no match for job with specified id
    def del_from_waiting(self, job_id, hwid):
        for job in self.que_list:
            if job.job_id == job_id:
                job.del_from_waiting(hwid)
                return True
        return False

    # returns list of jobs with empty wait list, used for deletion of completed jobs
    def get_empty(self):
        out = []
        for job in self.que_list:
            if len(job.waiting_for) == 0:
                out.append(job.job_id)
        return out
