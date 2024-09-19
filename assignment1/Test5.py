import time

n_operations = 25000000

dictionary = dict()

start = time.time()
for n in range(n_operations):
    dictionary[n] = n
end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
