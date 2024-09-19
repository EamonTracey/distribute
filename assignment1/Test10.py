import subprocess
import time

n_operations = 3456

start = time.time()
for _ in range(n_operations):
    subprocess.run(["ls", "-l"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
