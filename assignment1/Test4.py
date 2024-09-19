from datetime import datetime
import time

n_operations = 10000000

start = time.time()
for _ in range(n_operations):
    datetime.now().time()
end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
