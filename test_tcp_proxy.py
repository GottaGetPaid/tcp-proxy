import unittest
import socket
import threading
import time
import signal
from tcp_proxy import TcpProxy

class TestTcpProxy(unittest.TestCase):
    def setUp(self):
        self.proxy = TcpProxy(
            local_host="127.0.0.1",
            local_port=8080,
            remote_host="127.0.0.1",
            remote_port=9090
        )

    # verifies initial running state
    def test_proxy_initialization(self):
        self.assertEqual(self.proxy.local_host, "127.0.0.1")
        self.assertEqual(self.proxy.local_port, 8080)
        self.assertEqual(self.proxy.remote_host, "127.0.0.1")
        self.assertEqual(self.proxy.remote_port, 9090)
        self.assertTrue(hasattr(self.proxy, 'is_running'))
        self.assertTrue(self.proxy.is_running)

    def test_proxy_connection(self):
        # Start mock server
        mock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mock_server.bind(("127.0.0.1", 9090))
        mock_server.listen(1)

        # Create an event to control the proxy thread
        stop_event = threading.Event()

        def run_proxy():
            while not stop_event.is_set():
                try:
                    # Start proxy without signal handling
                    self.proxy.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.proxy.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.proxy.server.bind((self.proxy.local_host, self.proxy.local_port))
                    self.proxy.server.listen(5)
                    
                    client_socket, _ = self.proxy.server.accept()
                    self.proxy.handle_client(client_socket)
                except Exception:
                    break
        
        # Start proxy in background
        proxy_thread = threading.Thread(target=self.proxy.start)
        proxy_thread.daemon = True
        proxy_thread.start()
        
        # Give proxy time to start
        time.sleep(0.1)
        
        try:
            # Create client connection
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("127.0.0.1", 8080))
        
            # Accept connection on mock server
            server_conn, _ = mock_server.accept()
            
            # Test data transfer
            test_data = b"Hello, World!"
            client.send(test_data)
            received = server_conn.recv(1024)
            
            self.assertEqual(test_data, received)
        finally:
            # Cleanup
            stop_event.set()
            client.close()
            server_conn.close()
            mock_server.close()
            if self.proxy.server:
                self.proxy.server.close()

    def test_signal_handling(self):
        # Start proxy in background
        proxy_thread = threading.Thread(target=self.proxy.start)
        proxy_thread.daemon = True
        proxy_thread.start()
        
        # Give proxy time to start
        time.sleep(0.1)
        
        # Test SIGTERM handling
        self.proxy.signal_handler(signal.SIGTERM, None)
        self.assertFalse(self.proxy.is_running)
        
        # Verify server socket is closed
        self.assertIsNotNone(self.proxy.server)
        
        # Try to connect - should fail if server is properly closed
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.assertRaises(ConnectionRefusedError):
            client.connect(("127.0.0.1", 8080))
        client.close()

if __name__ == "__main__":
    unittest.main()

