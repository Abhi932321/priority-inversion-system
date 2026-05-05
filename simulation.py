# Priority Inversion Simulation Project

class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority


def scheduler(processes):
    return max(processes, key=lambda x: x.priority)


class Resource:
    def __init__(self):
        self.locked = False
        self.holder = None


print("Simulating priority inversion scenario...")
