from typing import Any


class SpreadSheet:

    def __init__(self):
        self._data = dict()

    def insert(self, row: int, col: int, value: int):
        if row < 1:
            raise ValueError(f"row {row} cannot be negative")
        if col < 1:
            raise ValueError(f"column {col} cannot be negative")

        self._data[(row, col)] = value

    def lookup(self, row: int, col: int) -> Any:
        if row < 1:
            raise ValueError(f"row {row} cannot be negative")
        if col < 1:
            raise ValueError(f"column {col} cannot be negative")

        if (row, col) not in self._data:
            return None

        return self._data[(row, col)]

    def remove(self, row: int, col: int):
        if row < 1:
            raise ValueError(f"row {row} cannot be negative")
        if col < 1:
            raise ValueError(f"column {col} cannot be negative")

        if (row, col) in self._data:
            del self._data[(row, col)]

    def query(self, row: int, col: int, width: int,
              height: int) -> list[list[Any]]:
        row_max, col_max = self.size()

        if row < 1:
            raise ValueError(f"row {row} cannot be negative")
        if col < 1:
            raise ValueError(f"col {col} cannot be negative")

        values = {}
        for (r, c) in self._data:
            if row <= r <= row + height - 1 and col <= c <= col + width - 1:
                values[(r, c)] = self._data[(r, c)]

        return values

    def size(self) -> tuple[int, int]:
        row_max = 0
        col_max = 0

        for (r, c) in self._data:
            row_max = max(row_max, r)
            col_max = max(col_max, c)

        return (row_max, col_max)
