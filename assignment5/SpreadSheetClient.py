import builtins
import json
import pickle
import socket
import urllib.request
import time
from typing import Any

NAMESERVER = "http://catalog.cse.nd.edu:9097/query.json"


class SpreadSheetClient:

    def __init__(self, name):
        self.name = name

        self._socket = None
        self._connect()

    def _rpc(func):

        def wrapper(self, *args, **kwargs):
            payload = func(self, *args, **kwargs)
            message = pickle.dumps(payload)
            while True:
                try:
                    self._send_message(message)
                    response = self._receive_response()
                    if response is None:
                        raise ConnectionError
                    break
                except Exception as exception:
                    print(
                        "Failed to contact server, attempting reconnect now"
                    )
                    self._connect()

            # Payload containing exception_name indicates we must raise an exception.
            payload = pickle.loads(response)
            if "exception_name" in payload:
                exception_name = payload["exception_name"]
                exception_message = payload["exception_message"]
                raise getattr(builtins, exception_name)(exception_message)

            # Otherwise, return the specified return value.
            return payload["return"]

        return wrapper

    def _send_message(self, message: bytes):
        length = len(message).to_bytes(4, byteorder="big")
        self._socket.sendall(length)
        self._socket.sendall(message)

    def _receive_response(self) -> bytes:
        length = self._socket.recv(4)
        if not length:
            return None

        length = int.from_bytes(length, byteorder="big")
        response = bytes()
        while len(response) < length:
            response += self._socket.recv(length - len(response))
        if not response:
            return None

        return response

    def _connect(self):
        if self._socket is not None:
            self._socket.close()

        timeout = 1
        while True:
            try:
                payload: dict
                with urllib.request.urlopen(NAMESERVER) as response:
                    payload = json.loads(response.read().decode())

                matches = []
                for data in payload:
                    if ("type" in data and "project" in data
                            and data["type"] == "spreadsheet"
                            and data["project"] == self.name):
                        matches.append(data)

                host = matches[0]["address"]
                port = matches[0]["port"]
                heard = int(matches[0]["lastheardfrom"])
                for match in matches:
                    if match["lastheardfrom"] > heard:
                        host = match["address"]
                        port = match["port"]
                        heard = int(match["lastheardfrom"])

                self._socket = socket.socket(socket.AF_INET,
                                             socket.SOCK_STREAM)
                self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self._socket.settimeout(5)
                self._socket.connect((host, port))
                break
            except Exception as exception:
                print(
                    f"Failed to connect to {self.name}, attempting reconnect in {timeout} seconds"
                )
                time.sleep(timeout)
                timeout *= 2

    @_rpc
    def insert(self, row: int, col: int, value: int):
        payload = {
            "function": "insert",
            "arguments": {
                "row": row,
                "col": col,
                "value": value
            }
        }
        return payload

    @_rpc
    def lookup(self, row: int, col: int) -> Any:
        payload = {"function": "lookup", "arguments": {"row": row, "col": col}}
        return payload

    @_rpc
    def remove(self, row: int, col: int):
        payload = {
            "function": "remove",
            "arguments": {
                "row": row,
                "col": col,
            }
        }
        return payload

    @_rpc
    def query(self, row: int, col: int, width: int,
              height: int) -> list[list[int]]:
        payload = {
            "function": "query",
            "arguments": {
                "row": row,
                "col": col,
                "width": width,
                "height": height
            }
        }
        return payload

    @_rpc
    def size(self) -> tuple[int, int]:
        payload = {"function": "size", "arguments": {}}
        return payload
