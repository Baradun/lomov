import time 
from multiprocessing import Process

start_time = time.time()
print('start')
list_process = []


def sl():
    time.sleep(2)
    print("закончил")

for i in range(10):
    list_process.append(Process(target=sl))

threads = 4
run_process = []
while len(list_process) != 0:
    if len(run_process) < threads and len(list_process) != 0:
        run_process.append(list_process.pop(0))
        run_process[len(run_process)-1].start()
        print('добавил')
        next
    
    for i in run_process:
        if not i.is_alive():
            run_process.remove(i)
    


while len(run_process) != 0:
    for i in run_process:
        if not i.is_alive():
            run_process.remove(i)


print("end")
print(time.time() - start_time)