import os
import time

n_operations = 7777

home = os.path.expanduser("~")

start = time.time()
for _ in range(n_operations):
    with os.scandir(home) as entries:
        for entry in entries:
            path = entry.path
            os.stat(path)

end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
