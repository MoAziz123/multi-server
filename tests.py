import socket
host = '127.0.0.1'
port = 80
def test_get():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send("POST postystuff".encode())
            assert(s.recv(8192).decode() == "ANSWER postystuff is really fun")
    except:
        print("POST test failed")

def test_post():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,port))
            s.send("GET chocolate".encode())
            assert(s.recv(8192).decode() == "ANSWER chocolate is a beautiful substance")
    except:
        print("GET test failed")

def test_delete():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,port))
            s.send("DELETE chocolate".encode())
            assert(s.recv(8192).decode() == "ANSWER chocolate is a beautiful substance")
    except:
        print("DELETE test failed")

def test_close():
    
try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,port))
            s.send("CLOSE".encode())
            assert(s.recv(8192).decode() == "Socket has been closed")
    except:
        print("CLOSE test failed")



def test_conn():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            assert(s.connect((host,port)) == True)
    except:
        print("Connection test failed")