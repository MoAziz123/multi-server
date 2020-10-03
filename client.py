import sys
import socket
import select

#for clients it's s

host = '127.0.0.1'
port = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print("Connected to", host, port)
    print("""
        --------------------------------
        Welcome to the HTTP Client - where you can send requests to a built server.
        Please type in commands below, of the following syntax:
            - GET - get something from the server
            - POST - post something securely to the server
            - DELETE - delete something from the server
            - PUT - update something from the server
            - OPTIONS - ???
            - CLOSE - quit the program
        --------------------------------
        """)
    while(True):
        data = input('Enter your command:  ')
        s.send(data.encode())
        print(s.recv(8192).decode())






