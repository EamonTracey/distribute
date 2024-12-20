import argparse
import time

import ClusterClient
import SpreadSheet
import SpreadSheetClient

SIZE = 50


def main(args: argparse.Namespace):
    name = args.name
    n = args.n
    k = args.k

    # spreadsheet = SpreadSheet.SpreadSheet()
    # spreadsheet = SpreadSheetClient.SpreadSheetClient(name)
    spreadsheet = ClusterClient.ClusterClient(name, n, k)
    data = {"rk": 4}

    # Test performance of insert.
    start = time.time()
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            spreadsheet.insert(i, j, data)
    end = time.time()
    insert_time = end - start

    # Test performance of lookup.
    start = time.time()
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            spreadsheet.lookup(i, j)
    end = time.time()
    lookup_time = end - start

    # Test performance of query.
    start = time.time()
    for _ in range(1, SIZE + 1):
        for __ in range(1, SIZE + 1):
            spreadsheet.query(1, 1, SIZE, SIZE)
    end = time.time()
    query_time = end - start


    # Test performance of remove.
    start = time.time()
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            spreadsheet.remove(i, j)
    end = time.time()
    remove_time = end - start

    # Test performance of size.
    start = time.time()
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            spreadsheet.size()
    end = time.time()
    size_time = end - start

    n_operations = SIZE * SIZE
    print(f"Insert ({n_operations})")
    print(f"    Time (s): {insert_time:.5f}")
    print(f"    Throughput (ops/s): {n_operations / insert_time:.5f}")
    print(f"    Latency (s): {insert_time / n_operations:.5f}")

    print(f"Lookup ({n_operations})")
    print(f"    Time (s): {lookup_time:.5f}")
    print(f"    Throughput (ops/s): {n_operations / lookup_time:.5f}")
    print(f"    Latency (s): {lookup_time / n_operations:.5f}")

    print(f"Query ({n_operations})")
    print(f"    Time (s): {query_time:.5f}")
    print(f"    Throughput (ops/s): {n_operations / query_time:.5f}")
    print(f"    Latency (s): {query_time / n_operations:.5f}")

    print(f"Remove ({n_operations})")
    print(f"    Time (s): {remove_time:.5f}")
    print(f"    Throughput (ops/s): {n_operations / remove_time:.5f}")
    print(f"    Latency (s): {remove_time / n_operations:.5f}")

    print(f"Size ({n_operations})")
    print(f"    Time (s): {size_time:.5f}")
    print(f"    Throughput (ops/s): {n_operations / size_time:.5f}")
    print(f"    Latency (s): {size_time / n_operations:.5f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("n", type=int)
    parser.add_argument("k", type=int)
    args = parser.parse_args()
    main(args)
