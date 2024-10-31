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
        # The hash can be extremely simple. Using addition means that cells
        # further from (1, 1) will be managed by higher-numbered servers
        # (until wraparound).
        hash_value = n1 + n2
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
