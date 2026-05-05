class Process:
    def __init__(self, pid, priority, arrival, burst, needs_resource=False):
        self.pid = pid
        self.base_priority = priority
        self.priority = priority
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.needs_resource = needs_resource
        self.state = "READY"

class Resource:
    def __init__(self, ceiling_priority):
        self.locked = False
        self.holder = None
        self.ceiling = ceiling_priority


def reset_states(processes):
    for p in processes:
        if p.remaining > 0:
            p.state = "READY"


def simulate_without_protocol():
    print("\n--- WITHOUT PROTOCOL ---")

    L = Process("L", 1, 0, 3, True)
    M = Process("M", 2, 2, 2)
    H = Process("H", 3, 1, 2, True)

    resource = Resource(3)
    processes = [L, H, M]
    time = 0

    while any(p.remaining > 0 for p in processes):

        reset_states(processes)

        ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

        for p in ready:
            if resource.locked and p.needs_resource and resource.holder != p:
                p.state = "BLOCKED"

        ready = [p for p in ready if p.state != "BLOCKED"]

        if ready:
            current = max(ready, key=lambda x: x.priority)

            if current.needs_resource and not resource.locked:
                resource.locked = True
                resource.holder = current

            if time == 2:
                print(">>> Priority Inversion Occurring (H blocked, M running)")

            print(f"Time {time}: {current.pid} RUNNING")
            current.remaining -= 1

            if current.remaining == 0 and resource.holder == current:
                resource.locked = False
                resource.holder = None
                print(f"Time {time}: Resource released by {current.pid}")

        else:
            print(f"Time {time}: CPU IDLE")

        time += 1


def simulate_pip():
    print("\n--- WITH PRIORITY INHERITANCE ---")

    L = Process("L", 1, 0, 3, True)
    M = Process("M", 2, 2, 2)
    H = Process("H", 3, 1, 2, True)

    resource = Resource(3)
    processes = [L, H, M]
    time = 0

    while any(p.remaining > 0 for p in processes):

        reset_states(processes)

        ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

        for p in ready:
            if resource.locked and p.needs_resource and resource.holder != p:
                p.state = "BLOCKED"
                resource.holder.priority = max(resource.holder.priority, p.priority)

        ready = [p for p in ready if p.state != "BLOCKED"]

        if ready:
            current = max(ready, key=lambda x: x.priority)

            if current.needs_resource and not resource.locked:
                resource.locked = True
                resource.holder = current

            print(f"Time {time}: {current.pid} RUNNING (Priority {current.priority})")
            current.remaining -= 1

            if current.remaining == 0 and resource.holder == current:
                resource.locked = False
                resource.holder = None
                print(f"Time {time}: Resource released by {current.pid}")

        else:
            print(f"Time {time}: CPU IDLE")

        time += 1


def simulate_pcp():
    print("\n--- WITH PRIORITY CEILING ---")

    L = Process("L", 1, 0, 3, True)
    M = Process("M", 2, 2, 2)
    H = Process("H", 3, 1, 2, True)

    resource = Resource(3)
    processes = [L, H, M]
    time = 0

    while any(p.remaining > 0 for p in processes):

        reset_states(processes)

        ready = [p for p in processes if p.arrival <= time and p.remaining > 0]

        for p in ready:
            if resource.locked and p.needs_resource and resource.holder != p:
                p.state = "BLOCKED"

        if resource.locked:
            resource.holder.priority = resource.ceiling

        ready = [p for p in ready if p.state != "BLOCKED"]

        if ready:
            current = max(ready, key=lambda x: x.priority)

            if current.needs_resource and not resource.locked:
                resource.locked = True
                resource.holder = current
                current.priority = resource.ceiling

            print(f"Time {time}: {current.pid} RUNNING (Priority {current.priority})")
            current.remaining -= 1

            if current.remaining == 0 and resource.holder == current:
                resource.locked = False
                resource.holder = None
                print(f"Time {time}: Resource released by {current.pid}")

        else:
            print(f"Time {time}: CPU IDLE")

        time += 1


simulate_without_protocol()
simulate_pip()
simulate_pcp()
