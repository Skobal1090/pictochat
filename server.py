import socket


HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with sock:   
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"Listening on port {PORT}...")

    conn, addr = sock.accept()
    print(conn)
    print(addr)
    with conn:
        data = conn.recv(1500)
        print(data)
