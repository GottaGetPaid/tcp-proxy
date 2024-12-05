import socket
import threading
import select
import argparse
import signal
import sys
import logging

# enables error messages to print to console
logging.basicConfig(level=logging.INFO) 

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
        self.server = None
        self.is_running = True

    def signal_handler(self, signum, frame):
        signal_name = signal.Signals(signum).name
        logging.info(f"\nReceived signal {signal_name}. Gracefully shutting down...")
        self.is_running = False
        if self.server:
            self.server.close()
        sys.exit(0)

    def handle_client(self, client_socket):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((self.remote_host, self.remote_port))

        while self.is_running:
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
                logging.error(f"Error: {e}")
                break

        client_socket.close()
        remote_socket.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.local_host, self.local_port))
        self.server.listen(5)

        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler) # CTRL-C interruption
        signal.signal(signal.SIGTERM, self.signal_handler) # "kill"/polite interruption

        while True:
            try:
                client_socket, _ = self.server.accept()
                proxy_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                proxy_thread.daemon = True
                proxy_thread.start()
            except socket.error:
                if self.is_running:
                    logging.error("Socket error occurred")

def main():
    parser = argparse.ArgumentParser(description='TCP Proxy Server')
    parser.add_argument('--ip', default='localhost', 
                    help='local IP address to bind to')
    parser.add_argument('--port', type=int, default=8080,
                    help='local port to bind to')
    parser.add_argument('--server', required=True,
                    help='remote server address and port')
    
    args = parser.parse_args()
    
    proxy = TcpProxy(
        local_host=args.ip,
        local_port=args.port,
        remote_host=args.server.split(":")[0], # split b.c. only accept one server arg
        remote_port=args.server.split(":")[1] 
    )
    
    print(f"Starting proxy server on {proxy.local_host}:{proxy.local_port}")
    print(f"Forwarding to {proxy.remote_host}:{proxy.remote_port}")
    proxy.start()

if __name__ == '__main__':
    main()