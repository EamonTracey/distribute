import argparse
import time

import SpreadSheet
import SpreadSheetClient

SIZE = 25


def main(args: argparse.Namespace):
    name = args.name

    # spreadsheet = SpreadSheet.SpreadSheet()
    spreadsheet = SpreadSheetClient.SpreadSheetClient(name)
    data = {"rk": 4}

    # Test performance of multiple inserts individually.
    insert_times = []
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            start = time.time()
            spreadsheet.insert(i, j, data)
            end = time.time()
            insert_times.append(end - start)

    # Test performance of multiple removes individually.
    remove_times = []
    for i in range(1, SIZE + 1):
        for j in range(1, SIZE + 1):
            start = time.time()
            spreadsheet.remove(i, j)
            end = time.time()
            remove_times.append(end - start)

    n_operations = SIZE * SIZE
    print(f"Insert ({n_operations})")
    print(f"    Minimum Time (s): {min(insert_times)}")
    print(f"    Maximum Time (s): {max(insert_times)}")
    print(f"    Average Time (s): {sum(insert_times) / len(insert_times)}")

    print(f"Remove ({n_operations})")
    print(f"    Minimum Time (s): {min(remove_times)}")
    print(f"    Maximum Time (s): {max(remove_times)}")
    print(f"    Average Time (s): {sum(remove_times) / len(remove_times)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    args = parser.parse_args()
    main(args)
