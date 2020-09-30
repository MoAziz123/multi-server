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
        await get(conn, rec_data)
    elif protocol == "post":
        await post(conn, rec_data)
    elif protocol == "delete":
        await delete(conn, rec_data)
    else:
        await error(conn, protocol)


async def error(conn, item):
    item_str = ' '.join(item) + "is not a valid function of the server"
    await conn.send(item_str.encode())
async def get(conn, item):
    item_str = ' '.join(item)
    try:
        await conn.send(("ANSWER " + items["get"][item_str]).encode())
    except:
        await conn.send(("Unable to find " + item_str + " in GET dictionary").encode())
async def post(conn, item):
    item_str = ' '.join(item)
    try:
       await conn.send(("ANSWER " + items["post"][item_str]).encode())
    except:
        await conn.send(("Unable to find " + item_str + " in POST dictionary").encode())

async def delete(conn, item):
    item_str = ' '.join(item)
    try:
        await conn.send(("ANSWER " + items["delete"][item_str]).encode())
    except:
        await conn.send(("Unable to find " + item_str + " in DELETE dictionary").encode())
#for server, it's conn
async def mainLoop():
    host, port = "127.0.0.1", 80
    print("Listening on", host, port)
    functions = ["get", "post", "delete"]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)
    conn, address = s.accept()
    with conn:
        while True:
            print("Connected to,", address)
            data = conn.recv(8192) #hits max byte limit
            await parseInput(conn, data.decode().split(" "))
            if ConnectionAbortedError:
                pass



loop = asyncio.get_event_loop()
loop.run_until_complete(mainLoop())
loop.close()
