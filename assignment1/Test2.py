import os
import time

n_operations = 1500

home = os.path.expanduser("~")
filename = os.path.join(home, ".distsys")

start = time.time()
for _ in range(n_operations):
    open(filename, "w")
    os.remove(filename)
end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
