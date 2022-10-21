#!/usr/bin/python3.10
# send_file.py - a script to send a file.

import socket
import argparse
from pathlib import Path

SEPARATOR = "<SEPARATOR>"


def get_arguments() -> argparse.Namespace:
    '''Setup and return argument parser arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Path of file to send.", type=str)
    parser.add_argument("host_ip", help="Host IP address", type=str)
    parser.add_argument("port", help="Port on the host to send the file.", type=int)
    parser.add_argument("-b", "--buffer-size", help="Buffersize to send file", type=int, default=4096)
    args = parser.parse_args()
    return args 


def main():

    args = get_arguments() 

    # setup main arguments
    host = args.host_ip
    port = args.port
    buffer_size = args.buffer_size
    filepath = Path(args.filepath)


    filesize = filepath.stat().st_size
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        # send filename, and file size first
        sock.send(f"{filepath.name}{SEPARATOR}{filesize}\n".encode())

        with filepath.open("rb") as efile:

            while True:
                bytes_read = efile.read(buffer_size)

                # files is done being read and empty
                if not bytes_read:
                    break

                sock.sendall(bytes_read)
        
        sock.shutdown(socket.SHUT_WR)


    print("Done Sending File.")





if __name__ == "__main__":
    main()