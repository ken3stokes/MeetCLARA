import ssl
import http.server
import socketserver
import threading
from pathlib import Path

class SecureHTTPServer:
    def __init__(self, host='localhost', port=4443):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
        
        # Generate self-signed certificate if not exists
        self.cert_path = Path(__file__).parent / 'test_cert.pem'
        self.key_path = Path(__file__).parent / 'test_key.pem'
        
    def create_ssl_context(self):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        context.load_cert_chain(certfile=str(self.cert_path), keyfile=str(self.key_path))
        return context
        
    def start(self):
        handler = http.server.SimpleHTTPRequestHandler
        self.server = socketserver.TCPServer((self.host, self.port), handler)
        
        # Wrap socket with SSL context
        self.server.socket = self.create_ssl_context().wrap_socket(
            self.server.socket,
            server_side=True
        )
        
        # Run server in a separate thread
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        print(f"Server running on https://{self.host}:{self.port}")
        
    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("Server stopped")

if __name__ == '__main__':
    server = SecureHTTPServer()
    try:
        server.start()
        input("Press Enter to stop the server...")
    finally:
        server.stop()
