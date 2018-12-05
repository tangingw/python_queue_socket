import json
import sys
import socketserver
import threading
import time
from queue import Queue


thread_num = 2


CONFIG = None
with open("json\\config.json") as json_config:

    CONFIG = json.loads(json_config.read())


channel_length = len(CONFIG["channel"])
channel_dict = { CONFIG["channel"][i]: Queue() for i in range(channel_length)}


def tcp_server(port):

    class QueueTCPHandler(socketserver.BaseRequestHandler):

        def setup(self):

            self.channel_dict = channel_dict

        def handle(self):

            while True:

                self.data = self.request.recv(1024).strip()

                if not self.data:
                
                    break

                decoded_data = json.loads(self.data.decode('utf-8'))
                self.channel_dict[decoded_data["channel"]].put(decoded_data["message"])

                self.request.sendall(self.data.upper())

    return socketserver.TCPServer(("0.0.0.0", port), QueueTCPHandler)


def main():


    port = 5566
    server = tcp_server(port)

    i = 0
    
    while i < thread_num:

        worker = threading.Thread(target=server.serve_forever)
        worker.setDaemon(True)
        worker.start()

        i += 1

    while True:

        for channel_name in channel_dict.keys():

            while not channel_dict[channel_name].empty():

                print(channel_dict[channel_name].get())
    
        time.sleep(1)


if __name__ == "__main__":

    main()