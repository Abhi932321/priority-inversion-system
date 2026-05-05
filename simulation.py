# Priority Inversion Simulation Project
class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority
        def scheduler(processes):
            return max(processes, key=lambda x: x.priority)
