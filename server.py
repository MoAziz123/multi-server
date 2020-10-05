import socket
import sys
import select
import asyncio
import _thread
import yaml

items = {"get":{"chocolate":"chocolate is a beautiful substance", "poison":"poision is a type of harmful substance made from nightshade"},
         "post":{"postystuff":"postystuff is really fun", "chicken":"chicken is a great meat"},
         "delete":{"ghost":"a dead thing", "ultraboss":"a scary entity"}}
with open('./config.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    web_dir = data['dir']
    host = data['host']
    port = data['port']
#@method - parseInput - takes input from client
#@description - takes each input and parses based on first word - standardized via .lower()
def parseInput(conn, lines):
    request = lines[0] #main line
    headers = lines[1] #headers
    if(len(lines)>3):
        conn.send("Maximum number of lines exceeded, should be 2 lines".encode())
    else:
        request = request.split(" ")
        method = request[0].lower()
        version = parseVersion(conn, request[2])
        resource= parseResource(conn,request[1], version)
        headers = parseHeaders(conn, headers)
        print(method, resource, version, headers)

    if method == "get":
       get(conn, resource)
    elif method == "post":
        post(conn, resource)
    elif method == "delete":
        delete(conn, resource)
    elif method == "close":
        close(conn)
    elif method == "put":
        put(conn, resource)
    elif method == "head":
        head(conn, resource)
    else:
        error(conn, method)
    conn.send("/*end of data*/".encode())

def close(conn):
    conn.send("Socket has been closed".encode())
    print("Socket "+ conn + " has been closed")
    conn.close()
    if ConnectionAbortedError:
        pass
def error(conn, item):
    item_str = "HTTP/1.0 400 Bad Request"
    conn.send(item_str.encode())

def get(conn, item):
    try:
        f = open(web_dir + item)
        conn.send(" ".join(f.readlines()).encode())
    except:
        error(conn, "GET")
def post(conn, item):
    item_str = ' '.join(item)
    try:
       encoded_item = ("ANSWER " + items["post"][item_str]).encode()
       conn.send(encoded_item)
    except:
        conn.send(("Unable to find " + item_str + " in POST dictionary").encode())

def delete(conn, item):
    item_str = ' '.join(item)#
    try:
        for key, value in items:
            print(key, value)
        conn.send(("ANSWER - " + item_str).encode() + " has been deleted")
    except:
        conn.send(("Unable to find " + item_str + " in DELETE dictionary").encode())

def put(conn, item):
    #put distinction between file and var
    items_str = ' '.join(item)
    print(items_str)

def head(conn, item):
    print("head")

def parseResource(conn, resource, version):
    #error codes for 200, 400, 404
    try:
        f = open(web_dir + resource)
        conn.send((version + " 200 OK").encode())
        return resource
    except IOError:
        conn.send((version + " 404 - FILE NOT FOUND").encode())
        return resource, None

    

def parseVersion(conn,version):
    if("HTTP/" not in version):
        conn.send("Please include the HTTP/ prefix to the version.")
    return version

def parseHeaders(conn, headers):
    if len(headers)  < 1:
        return ""
    headers_dict = {}
    headers = headers.split(":")
    for i in range(0, len(headers)):
        if i % 2 == 0:
            headers_dict.update({headers[i]:headers[i+1]})
        break
    for key, value in headers_dict.items():
        conn.send((key + ": " + value).encode())
    return headers_dict


    


#@method - handleconn - takes in server socket and address as parameters
#@description - runs loop which takes in connections and allows them to run async
def handleconn(conn, addr):
 while True:
        if ConnectionAbortedError:
                pass
        print("Connected to,", addr)
        data = conn.recv(8192)
        lines = data.decode().split("\r\n")
        print(lines)
        try:
            parseInput(conn, lines)
        except socket.error as e :
            conn.send("ERROR - " + str(e))
        
def mainLoop():
    print("Listening on", host, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(10)
    while True:
        conn, addr = server.accept()
        _thread.start_new_thread(handleconn, (conn, addr))
    server.close()
   



mainLoop()