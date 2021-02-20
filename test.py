import time 
from multiprocessing import Process, Pool

start_time = time.time()
print('start')
list_process = []


def sl(i):
    time.sleep(i)
    print(f"закончил {i}")

for i in range(10):
    list_process.append(i)

# threads = 4
# run_process = []
# while len(list_process) != 0:
#     if len(run_process) < threads and len(list_process) != 0:
#         run_process.append(list_process.pop(0))
#         run_process[len(run_process)-1].start()
#         print('добавил')
#         next
    
#     for i in run_process:
#         if not i.is_alive():
#             run_process.remove(i)
    


# while len(run_process) != 0:
#     for i in run_process:
#         if not i.is_alive():
#             run_process.remove(i)

p = Pool(10)
p.map(sl, list_process)


print("end")
print(time.time() - start_time)