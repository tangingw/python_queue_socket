import json
import socket
import time

def encode_msg(channel, message):

    return json.dumps(
        {
            "channel": channel,
            "message": message
        }
    ).encode('utf-8')


def main():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect(('10.51.130.183', 5566))

        while True:

            current_time_str = str(time.time())
            #s.sendall(('testing hahacd34 %s' % str(time.time())).encode('utf-8'))
            s.sendall(encode_msg('furball', 'testing hahacd34 %s' % current_time_str))
            s.sendall(encode_msg('firebase', 'yahoo %s' % current_time_str))
            time.sleep(2)
            data = s.recv(1024)

            print(repr(data))


if __name__ == "__main__":

    main()