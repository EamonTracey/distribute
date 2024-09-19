import socket
import time

n_operations = 250

host = "www.google.com"
port = 80

start = time.time()
for _ in range(n_operations):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.close()
end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
