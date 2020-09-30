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
        print("GET test passed")
