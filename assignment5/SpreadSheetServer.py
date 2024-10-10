import argparse
import json
import os
import pickle
import select
import socket
import time
import threading

from SpreadSheet import SpreadSheet

INVALID_REQUEST_RESPONSE = pickle.dumps({
    "exception_name":
    "ValueError",
    "exception_message":
    "an invalid or unsupported request was received"
})

NAMESERVER_HOST = "catalog.cse.nd.edu"
NAMESERVER_PORT = 9097


class SpreadSheetServer:

    def __init__(self, name: str):
        self.name = name

        open("sheet.log", "ab").close()
        self._load_checkpoint()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(("0.0.0.0", 0))
        self._socket.listen()
        self.port = self._socket.getsockname()[1]
        print(f"Listening on port {self.port}")

        self._update_nameserver()

    def _update_nameserver(self):
        payload = {
            "type": "spreadsheet",
            "owner": "etracey",
            "port": self.port,
            "project": self.name
        }
        message = json.dumps(payload).encode()

        # Send our message to the nameserver.
        nameserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        nameserver.sendto(message, (NAMESERVER_HOST, NAMESERVER_PORT))

        # Launch a thread to perform this function again in 60 seconds.
        timer = threading.Timer(60, self._update_nameserver)
        timer.daemon = True
        timer.start()

    def _load_checkpoint(self):
        try:
            with open("sheet.ckpt", "rb") as fp:
                self.spreadsheet = pickle.load(fp)
        except Exception as exception:
            # If there is any issue loading the checkpoint file,
            # then start with a blank sheet.
            self.spreadsheet = SpreadSheet()

        self._log_size = 0
        with open("sheet.log", "rb+") as fp:
            while True:
                try:
                    position = fp.tell()
                    payload = pickle.load(fp)
                    function = payload["function"]
                    arguments = payload["arguments"]
                    getattr(self.spreadsheet, function)(**arguments)
                    self._log_size += 1
                except Exception as exception:
                    fp.truncate(position)
                    break

    def _dump_checkpoint(self):
        # Dump the checkpoint.
        with open(".sheet.ckpt", "wb") as fp:
            pickle.dump(self.spreadsheet, fp)
            fp.flush()
            os.fsync(fp)
        os.rename(".sheet.ckpt", "sheet.ckpt")

        # Truncate the log.
        with open("sheet.log", "wb") as fp:
            fp.truncate(0)
        self._log_size = 0

    def _log_payload(self, payload: dict):
        with open("sheet.log", "ab") as fp:
            pickle.dump(payload, fp)
            fp.flush()
            os.fsync(fp)
        self._log_size += 1

    def _receive_message(self, connection: socket.socket) -> bytes:
        length = connection.recv(4)
        if not length:
            return None

        length = int.from_bytes(length, byteorder="big")
        message = bytes()
        while len(message) < length:
            message += connection.recv(length - len(message))
        if not message:
            return None

        return message

    def _generate_response(self, message: bytes) -> bytes:
        try:
            payload = pickle.loads(message)
        except pickle.PickleError:
            return INVALID_REQUEST_RESPONSE

        if type(payload) is not dict or len(
                payload
        ) != 2 or "function" not in payload or "arguments" not in payload:
            return INVALID_REQUEST_RESPONSE

        function = payload["function"]
        arguments = payload["arguments"]
        return_value = None
        exception_name = None
        exception_message = None
        try:
            return_value = getattr(self.spreadsheet, function)(**arguments)
        except Exception as exception:
            exception_name = type(exception).__name__
            exception_message = str(exception)

        if exception_name is None:
            if function == "insert" or function == "remove":
                self._log_payload(payload)

        payload = {}
        if exception_name is None:
            payload["return"] = return_value
        else:
            payload["exception_name"] = exception_name
            payload["exception_message"] = exception_message

        response = pickle.dumps(payload)
        return response

    def _send_response(self, response: bytes, connection: socket.socket):
        length = len(response).to_bytes(4, byteorder="big")
        connection.sendall(length)
        connection.sendall(response)

    def run(self):
        while True:
            if self._log_size > 100:
                self._dump_checkpoint()

            connection, _ = self._socket.accept()
            while True:
                try:
                    # Receive a message from the connected user.
                    message = self._receive_message(connection)

                    # If message is None, the connection has been closed.
                    if message is None:
                        break

                    if self._log_size > 100:
                        self._dump_checkpoint()

                    # Generate the response to the RPC.
                    response = self._generate_response(message)

                    # Send the response back to the connected user.
                    self._send_response(response, connection)
                except Exception:
                    pass


def main(args: argparse.Namespace):
    name = args.name

    spreadsheet_server = SpreadSheetServer(name)
    spreadsheet_server.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str)
    args = parser.parse_args()

    main(args)
