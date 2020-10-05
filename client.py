import sys
import socket
import select
import yaml


with open('./www/config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    host = data['host']
    port = data['port']
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
    while True:
        data = input('Enter your command:  ') + "\r\n"
        headers = input("Enter your headers: ") + "\r\n"
        s.send((data+headers).encode())
        while True: #gets all data until done
            item = s.recv(8192).decode()
            if(item == "/*end of data*/"):
                break
            print(item)
            






