import http.client
import time

n_operations = 150

host = "www.example.com"

start = time.time()
for _ in range(n_operations):
    connection = http.client.HTTPConnection(host)
    connection.request("GET", "/")
    response = connection.getresponse()
    response.read().decode("utf-8")

end = time.time()

elapsed = end - start

print(f"Elapsed time (s): {elapsed}")
print(f"Number of operations: {n_operations}")
print(f"Average time per operation (s): {elapsed / n_operations}")
