import socket
import threading
import select

def hex_dump(data, length=16):
    def char_print(byte):
        if 32 <= byte <= 126:
            return chr(byte)
        return '.'
    
    result = []
    for i in range(0, len(data), length):
        chunk = data[i:i + length]
        hex_line = ' '.join(f'{b:02x}' for b in chunk)
        printable = ''.join(char_print(b) for b in chunk)
        result.append(f"{i:04x}  {hex_line:<{length*3}}  {printable}")
    return '\n'.join(result)

class TcpProxy:
    def __init__(self, local_host="localhost", local_port=8080, 
                 remote_host="google.com", remote_port=80):
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.buffer_size = 4096

    def handle_client(self, client_socket):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((self.remote_host, self.remote_port))

        while True:
            try:
                readable, _, _ = select.select([client_socket, remote_socket], [], [])
                
                for sock in readable:
                    data = sock.recv(self.buffer_size)
                    if not data:
                        return
                    
                    direction = ">> " if sock is client_socket else "<< "
                    print(f"\n{direction}Traffic {len(data)} bytes:")
                    print(hex_dump(data))

                    if sock is client_socket:
                        remote_socket.send(data)
                    else:
                        client_socket.send(data)
            except Exception as e:
                print(f"Error: {e}")
                break

        client_socket.close()
        remote_socket.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.local_host, self.local_port))
        server.listen(5)

        while True:
            client_socket, _ = server.accept()
            proxy_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            proxy_thread.daemon = True
            proxy_thread.start()
