# devices queue
class Que:
    def __init__(self):
        self.queue = []

    def add_job(self, job):
        self.queue.append(job)

    # casing to string should give all jobs separated by a comma
    def __str__(self):
        ret_list = ""
        for job in self.queue:
            ret_list += str(job) + ' ,'
        return ret_list
