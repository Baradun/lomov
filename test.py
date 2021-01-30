import time 
from multiprocessing import Process

start_time = time.time()
print('start')
list_process = []


def sl():
    time.sleep(1)

for i in range(10):
    list_process.append(Process(target=sl))

cores = 4
run_process = []
while len(list_process) != 0:
    if len(run_process) < cores:
        run_process.append(list_process.pop(0))
        run_process[len(run_process)-1].start()
        

# print(list_process[0].is_alive())
# print(list_process[0].start())
# print(list_process[0].is_alive())
# time.sleep(2)
# print(list_process[0].is_alive())



print("end")
print(time.time() - start_time)