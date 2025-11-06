import socket


HOST = '0.0.0.0'
PORT = 8000

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
