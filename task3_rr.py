import copy
from collections import deque
from jobs import JOBS

def run_rr(quantum):
    jobs = copy.deepcopy(JOBS)
    for j in jobs:
        j["remaining_time"] = j["burst_time"]
        j["completion_time"] = 0

    jobs_by_arrival = sorted(jobs, key=lambda x: (x["arrival_time"], x["job_id"]))
    
    current_time = 0
    ready_queue = deque()
    unarrived = list(jobs_by_arrival)
    
    context_switches = 0
    last_job_id = None
    
    while unarrived or ready_queue:
        # Check newly arrived jobs at current_time
        newly_arrived = [j for j in unarrived if j["arrival_time"] <= current_time]
        for j in newly_arrived:
            ready_queue.append(j)
            unarrived.remove(j)
            
        if not ready_queue:
            if unarrived:
                current_time = unarrived[0]["arrival_time"]
                continue

        curr = ready_queue.popleft()
        
        if last_job_id is not None and last_job_id != curr["job_id"]:
            context_switches += 1
        last_job_id = curr["job_id"]
        
        exec_time = min(quantum, curr["remaining_time"])
        
        # Advance time step by step to handle arrivals during execution
        for _ in range(exec_time):
            current_time += 1
            curr["remaining_time"] -= 1
            
            # Check arrivals at exact tick
            arrivals_at_tick = [j for j in unarrived if j["arrival_time"] == current_time]
            for j in arrivals_at_tick:
                ready_queue.append(j)
                unarrived.remove(j)
                
        if curr["remaining_time"] > 0:
            ready_queue.append(curr)
        else:
            curr["completion_time"] = current_time

    avg_wt = sum(j["completion_time"] - j["arrival_time"] - j["burst_time"] for j in jobs) / len(jobs)
    avg_tat = sum(j["completion_time"] - j["arrival_time"] for j in jobs) / len(jobs)
    
    return avg_wt, avg_tat, context_switches

if __name__ == "__main__":
    wt3, tat3, cs3 = run_rr(3)
    wt6, tat6, cs6 = run_rr(6)
    print(f"Quantum 3 -> Avg WT: {wt3:.2f}, Avg TAT: {tat3:.2f}, Context Switches: {cs3}")
    print(f"Quantum 6 -> Avg WT: {wt6:.2f}, Avg TAT: {tat6:.2f}, Context Switches: {cs6}")
