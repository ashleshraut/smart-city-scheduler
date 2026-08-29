import copy
from jobs import JOBS

def run_fcfs(jobs):
    jobs = copy.deepcopy(jobs)
    jobs.sort(key=lambda x: (x["arrival_time"], x["job_id"]))
    
    current_time = 0
    results = []
    for j in jobs:
        if current_time < j["arrival_time"]:
            current_time = j["arrival_time"]
        start_time = current_time
        completion_time = start_time + j["burst_time"]
        turnaround_time = completion_time - j["arrival_time"]
        waiting_time = turnaround_time - j["burst_time"]
        current_time = completion_time
        results.append({
            "job_id": j["job_id"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })
    return results

def run_sjf(jobs):
    jobs = copy.deepcopy(jobs)
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
            
        ready.sort(key=lambda x: (x["burst_time"], x["arrival_time"], x["job_id"]))
        curr = ready.pop(0)
        
        start_time = current_time
        completion_time = start_time + curr["burst_time"]
        turnaround_time = completion_time - curr["arrival_time"]
        waiting_time = turnaround_time - curr["burst_time"]
        current_time = completion_time
        
        completed.append({
            "job_id": curr["job_id"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })
    return completed

def run_srtf(jobs):
    jobs = copy.deepcopy(jobs)
    for j in jobs:
        j["remaining_time"] = j["burst_time"]
        j["first_start"] = -1
        j["completion_time"] = 0
        
    current_time = 0
    completed_count = 0
    n = len(jobs)
    
    while completed_count < n:
        ready = [j for j in jobs if j["arrival_time"] <= current_time and j["remaining_time"] > 0]
        if not ready:
            current_time += 1
            continue
            
        ready.sort(key=lambda x: (x["remaining_time"], x["arrival_time"], x["job_id"]))
        curr = ready[0]
        
        curr["remaining_time"] -= 1
        current_time += 1
        
        if curr["remaining_time"] == 0:
            completed_count += 1
            curr["completion_time"] = current_time

    results = []
    for j in jobs:
        tat = j["completion_time"] - j["arrival_time"]
        wt = tat - j["burst_time"]
        results.append({
            "job_id": j["job_id"],
            "waiting_time": wt,
            "turnaround_time": tat
        })
    return results

if __name__ == "__main__":
    for name, fn in [("FCFS", run_fcfs), ("SJF", run_sjf), ("SRTF", run_srtf)]:
        res = fn(JOBS)
        avg_wt = sum(r["waiting_time"] for r in res) / len(res)
        avg_tat = sum(r["turnaround_time"] for r in res) / len(res)
        print(f"=== {name} ===")
        for r in res:
            print(f"Job: {r['job_id']} | Waiting: {r['waiting_time']} | Turnaround: {r['turnaround_time']}")
        print(f"Average Waiting Time: {avg_wt:.2f}")
        print(f"Average Turnaround Time: {avg_tat:.2f}\n")
