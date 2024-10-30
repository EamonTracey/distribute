import math
import time
from typing import Any

from SpreadSheetClient import SpreadSheetClient


class ClusterClient:

    def __init__(self, name, n, k):
        assert 1 <= k <= n

        self.name = name
        self.n = n
        self.k = k

        self._clients = [SpreadSheetClient(f"{name}-{i}") for i in range(n)]

    @staticmethod
    def _hash(n1: int, n2: int):
        # Convert the 2 integers to a string of bytes.
        data = n1.to_bytes((n1.bit_length() + 7) // 8, signed=True) + n2.to_bytes(
            (n2.bit_length() + 7) // 8, signed=True)

        # Apply the FNV-1a hash function.
        fnv_prime = 0x01000193
        hash_value = 0x811c9dc5
        upper_bound = 2**32
        for byte in data:
            hash_value ^= byte
            hash_value = (hash_value * fnv_prime) % upper_bound

        return hash_value

    def insert(self, row: int, col: int, value: int):
        base = ClusterClient._hash(row, col) % self.n
        result = None
        for i in range(self.k):
            client = self._clients[(base + i) % self.n]
            while True:
                try:
                    result = client.insert(row, col, value)
                    break
                except ConnectionError:
                    time.sleep(5)
        return result

    def lookup(self, row: int, col: int) -> Any:
        while True:
            base = ClusterClient._hash(row, col) % self.n
            for i in range(self.k):
                client = self._clients[(base + i) % self.n]
                try:
                    result = client.lookup(row, col)
                    return result
                except ConnectionError:
                    pass
            time.sleep(5)

    def remove(self, row: int, col: int):
        base = ClusterClient._hash(row, col) % self.n
        result = None
        for i in range(self.k):
            client = self._clients[(base + i) % self.n]
            while True:
                try:
                    result = client.remove(row, col)
                    break
                except ConnectionError:
                    time.sleep(5)
        return result

    def query(self, row: int, col: int, width: int,
              height: int) -> list[list[int]]:
        result_final = {}
        for client in self._clients:
            while True:
                try:
                    result = client.query(row, col, width, height)
                    result_final |= result
                    break
                except ConnectionError:
                    time.sleep(5)
        return result_final

    def size(self) -> tuple[int, int]:
        result_final = (0, 0)
        for client in self._clients:
            while True:
                try:
                    result = client.size()
                    result_final = (max(result_final[0], result[0]),
                                    max(result_final[1], result[1]))
                    break
                except ConnectionError:
                    time.sleep(5)
        return result_final
