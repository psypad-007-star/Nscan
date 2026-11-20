import socket
import threading

def mock_service(ip, port, banner):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen()
        while True:
            conn, _ = s.accept()
            with conn:
                conn.sendall(banner.encode())

# Simulate 3 different "hosts" on the loopback subnet
targets = [
    ("127.0.0.1", 8080, "HTTP/1.1 200 OK\r\nServer: MockWeb\r\n\r\n"),
    ("127.0.0.2", 2222, "SSH-2.0-OpenSSH_Mock\r\n"),
    ("127.0.0.3", 9000, "Mock-Database-Ready\r\n"),
]

for ip, port, banner in targets:
    threading.Thread(target=mock_service, args=(ip, port, banner), daemon=True).start()

input("Simulated hosts running on 127.0.0.1-3. Press Enter to stop...\n")
