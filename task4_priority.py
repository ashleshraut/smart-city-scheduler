import copy
from jobs import JOBS

def run_priority_no_aging():
    jobs = copy.deepcopy(JOBS)
    completed = []
    current_time = 0
    ready = []
    unarrived = list(jobs)
    
    while unarrived or ready:
        newly_arrived = [j for j in unarrived if j["arrival_time"] <= current_time]
        for j in newly_arrived:
            ready.append(j)
            unarrived.remove(j)
            
        if not ready:
            current_time = min(j["arrival_time"] for j in unarrived)
            continue
            
        ready.sort(key=lambda x: (x["priority"], x["arrival_time"], x["job_id"]))
        curr = ready.pop(0)
        
        start_time = current_time
        completion_time = start_time + curr["burst_time"]
        wt = start_time - curr["arrival_time"]
        tat = completion_time - curr["arrival_time"]
        current_time = completion_time
        
        completed.append({"job_id": curr["job_id"], "wt": wt, "tat": tat})
    return completed

def run_priority_aging():
    jobs = copy.deepcopy(JOBS)
    for j in jobs:
        j["ready_since"] = None
        
    completed = []
    current_time = 0
    ready = []
    unarrived = list(jobs)
    
    while unarrived or ready:
        newly_arrived = [j for j in unarrived if j["arrival_time"] <= current_time]
        for j in newly_arrived:
            j["ready_since"] = j["arrival_time"]
            ready.append(j)
            unarrived.remove(j)
            
        if not ready:
            current_time = min(j["arrival_time"] for j in unarrived)
            continue
            
        for j in ready:
            ticks_waited = current_time - j["ready_since"]
            j["effective_priority"] = max(1, j["priority"] - (ticks_waited // 3))
            
        ready.sort(key=lambda x: (x["effective_priority"], x["arrival_time"], x["job_id"]))
        curr = ready.pop(0)
        
        start_time = current_time
        completion_time = start_time + curr["burst_time"]
        wt = start_time - curr["arrival_time"]
        tat = completion_time - curr["arrival_time"]
        current_time = completion_time
        
        completed.append({"job_id": curr["job_id"], "wt": wt, "tat": tat})
    return completed

if __name__ == "__main__":
    no_aging = run_priority_no_aging()
    aging = run_priority_aging()
    
    print("=== No Aging ===")
    for r in no_aging:
        print(f"Job: {r['job_id']}, WT: {r['wt']}, TAT: {r['tat']}")
        
    print("\n=== With Aging ===")
    for r in aging:
        print(f"Job: {r['job_id']}, WT: {r['wt']}, TAT: {r['tat']}")
