import builtins
import json
import pickle
import socket
import urllib.request
from typing import Any

NAMESERVER = "http://catalog.cse.nd.edu:9097/query.json"


class SpreadSheetClient:

    def __init__(self, name):
        self.name = name

        self._connect()

    def _rpc(func):

        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)

            # If the response is None, we have lost connection with the server.
            if response is None:
                raise ConnectionError("lost connection with the server")

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
        payload: dict
        with urllib.request.urlopen(NAMESERVER) as response:
            payload = json.loads(response.read().decode())

        matches = []
        for data in payload:
            if ("type" in data and "project" in data
                    and data["type"] == "spreadsheet"
                    and data["project"] == self.name):
                matches.append(data)

        if not matches:
            ...

        host = matches[0]["address"]
        port = matches[0]["port"]
        heard = int(matches[0]["lastheardfrom"])
        for match in matches:
            if match["lastheardfrom"] > heard:
                host = match["address"]
                port = match["port"]
                heard = int(match["lastheardfrom"])

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.host, self.port))

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
        message = pickle.dumps(payload)
        self._send_message(message)
        response = self._receive_response()
        return response

    @_rpc
    def lookup(self, row: int, col: int) -> Any:
        payload = {"function": "lookup", "arguments": {"row": row, "col": col}}
        message = pickle.dumps(payload)
        self._send_message(message)
        response = self._receive_response()
        return response

    @_rpc
    def remove(self, row: int, col: int):
        payload = {
            "function": "remove",
            "arguments": {
                "row": row,
                "col": col,
            }
        }
        message = pickle.dumps(payload)
        self._send_message(message)
        response = self._receive_response()
        return response

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
        message = pickle.dumps(payload)
        self._send_message(message)
        response = self._receive_response()
        return response

    @_rpc
    def size(self) -> tuple[int, int]:
        payload = {"function": "size", "arguments": {}}
        message = pickle.dumps(payload)
        self._send_message(message)
        response = self._receive_response()
        return response
