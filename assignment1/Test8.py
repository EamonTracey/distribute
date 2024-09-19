import json
import time

n_operations = 1500

filename = "licenses.json"

start = time.time()
for _ in range(n_operations):
    fp = open(filename)
    json.load(fp)
    fp.close()

end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
