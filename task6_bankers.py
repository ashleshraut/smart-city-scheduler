import copy

AVAILABLE = [3, 3, 2]
MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2]
}
ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1]
}

def calculate_need():
    need = {}
    for p in MAX_NEED:
        need[p] = [MAX_NEED[p][i] - ALLOCATION[p][i] for i in range(3)]
    return need

def is_safe_state(avail, alloc, need):
    work = list(avail)
    finish = {p: False for p in alloc}
    safe_sequence = []

    while len(safe_sequence) < len(alloc):
        found = False
        for p in sorted(alloc.keys()):
            if not finish[p]:
                if all(need[p][i] <= work[i] for i in range(3)):
                    work = [work[i] + alloc[p][i] for i in range(3)]
                    finish[p] = True
                    safe_sequence.append(p)
                    found = True
                    break
        if not found:
            return False, []
    return True, safe_sequence

def evaluate_request(p_id, req):
    need = calculate_need()
    
    # Check 1: Request <= Need
    if any(req[i] > need[p_id][i] for i in range(3)):
        return False, "Error: Process exceeded max claim."
        
    # Check 2: Request <= Available
    if any(req[i] > AVAILABLE[i] for i in range(3)):
        return False, "Denied: Resources not available (availability-check failure)."
        
    # Pretend allocation
    temp_avail = [AVAILABLE[i] - req[i] for i in range(3)]
    temp_alloc = copy.deepcopy(ALLOCATION)
    temp_alloc[p_id] = [temp_alloc[p_id][i] + req[i] for i in range(3)]
    temp_need = copy.deepcopy(need)
    temp_need[p_id] = [temp_need[p_id][i] - req[i] for i in range(3)]
    
    safe, seq = is_safe_state(temp_avail, temp_alloc, temp_need)
    if safe:
        return True, f"Granted: System remains safe. Safe sequence: {seq}"
    else:
        return False, f"Denied: Granting request leads to an UNSAFE state (potential deadlock)."

if __name__ == "__main__":
    need_matrix = calculate_need()
    print("Need Matrix:")
    for p, n in need_matrix.items():
        print(f"{p}: {n}")
        
    safe, seq = is_safe_state(AVAILABLE, ALLOCATION, need_matrix)
    print(f"\nInitial State Safe: {safe}, Sequence: {seq}")
    
    print("\nEvaluating Request (a) P1 requests [1, 0, 2]:")
    res_a, msg_a = evaluate_request("P1", [1, 0, 2])
    print(msg_a)
    
    print("\nEvaluating Request (b) P0 requests [2, 0, 2]:")
    res_b, msg_b = evaluate_request("P0", [2, 0, 2])
    print(msg_b)
