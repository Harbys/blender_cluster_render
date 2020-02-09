class Que:
    def __init__(self):
        self.queue = []

    def add_job(self, job):
        self.queue.append(job)

    def __str__(self):
        ret_list = ""
        for job in self.queue:
            ret_list += str(job) + ' ,'
        return ret_list
