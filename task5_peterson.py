import time
import threading

shared_counter = 100

def thread_subtract_unshared():
    global shared_counter
    temp = shared_counter
    time.sleep(0.001)
    shared_counter = temp - 40

def thread_add_unshared():
    global shared_counter
    temp = shared_counter
    time.sleep(0.001)
    shared_counter = temp + 25

def run_unshared_demo():
    print("--- Unsynchronized Counter Runs ---")
    results = []
    for i in range(5):
        global shared_counter
        shared_counter = 100
        t1 = threading.Thread(target=thread_subtract_unshared)
        t2 = threading.Thread(target=thread_add_unshared)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        results.append(shared_counter)
        print(f"Run {i+1}: Final Value = {shared_counter}")
    return results

flag = [False, False]
turn = 0

def thread_subtract_peterson(process_id):
    global shared_counter, flag, turn
    other = 1 - process_id
    flag[process_id] = True
    turn = other
    while flag[other] and turn == other:
        pass
    
    # Critical Section
    temp = shared_counter
    time.sleep(0.001)
    shared_counter = temp - 40
    
    flag[process_id] = False

def thread_add_peterson(process_id):
    global shared_counter, flag, turn
    other = 1 - process_id
    flag[process_id] = True
    turn = other
    while flag[other] and turn == other:
        pass
    
    # Critical Section
    temp = shared_counter
    time.sleep(0.001)
    shared_counter = temp + 25
    
    flag[process_id] = False

def run_peterson_demo():
    print("\n--- Peterson's Algorithm Protected Runs ---")
    results = []
    for i in range(5):
        global shared_counter, flag, turn
        shared_counter = 100
        flag = [False, False]
        turn = 0
        t1 = threading.Thread(target=thread_subtract_peterson, args=(0,))
        t2 = threading.Thread(target=thread_add_peterson, args=(1,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        results.append(shared_counter)
        print(f"Run {i+1}: Final Value = {shared_counter}")
    return results

if __name__ == "__main__":
    run_unshared_demo()
    run_peterson_demo()
