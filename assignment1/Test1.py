import time

n_operations = 60000000

def trivial_function():
    pass

start = time.time()
for _ in range(n_operations):
    trivial_function()
end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
