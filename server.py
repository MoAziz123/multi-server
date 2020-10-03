import socket
import sys
import select
import asyncio
items = {"get":{"chocolate":"chocolate is a beautiful substance", "poison":"poision is a type of harmful substance made from nightshade"},
         "post":{"postystuff":"postystuff is really fun", "chicken":"chicken is a great meat"},
         "delete":{"ghost":"a dead thing", "ultraboss":"a scary entity"}}
async def parseInput(conn, args):
    protocol = args[0].lower()
    rec_data = args[1:len(args)]
    if protocol == "get":
        get(conn, rec_data)
    elif protocol == "post":
        post(conn, rec_data)
    elif protocol == "delete":
        delete(conn, rec_data)
    else:
        error(conn, protocol)


def error(conn, item):
    item_str = item.upper() + " is not a valid function of the server"
    conn.send(item_str.encode())
def get(conn, item):
    item_str = ' '.join(item)
    try:
        encoded_item = ("ANSWER " + items["get"][item_str]).encode()
        conn.send(encoded_item)
    except:
        conn.send(("Unable to find " + item_str + " in GET dictionary").encode())
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
            if items[key][value] == item:
                del items[key][value]
        conn.send(("ANSWER - " + item_str).encode() + " has been deleted")
    except:
        conn.send(("Unable to find " + item_str + " in DELETE dictionary").encode())
#for server, it's conn
async def handleconn(conn, addr):
 while True:
        if ConnectionAbortedError:
                pass
        print("Connected to,", addr)
        data = conn.recv(8192) #hits max byte limit
        await loop.create_task(parseInput(conn, data.decode().split(" ")))
        
async def mainLoop():
    host, port = "127.0.0.1", 80
    print("Listening on", host, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(10)
    while True:
        conn, addr = server.accept()
        await handleconn(conn, addr)
   



loop = asyncio.get_event_loop()
loop.run_until_complete(mainLoop())
loop.close()
