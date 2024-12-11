import unittest
import ssl
import threading
import time
import sys
from pathlib import Path
from app import check_domain_security

# Add the tests directory to the Python path
sys.path.append(str(Path(__file__).parent))
from test_server import SecureHTTPServer

class TestSSLConfiguration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start test server
        cls.server = SecureHTTPServer(port=4443)
        cls.server.start()
        # Give the server a moment to start
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        # Stop test server
        cls.server.stop()
        
    def test_secure_connection(self):
        """Test that we can establish a secure connection with TLS 1.2+"""
        result = check_domain_security('localhost')
        self.assertTrue(result['success'])
        self.assertIn(result['ssl_version'], ['TLSv1.2', 'TLSv1.3'])
        
    def test_certificate_validation(self):
        """Test certificate validation"""
        result = check_domain_security('localhost')
        self.assertTrue(result['success'])
        self.assertIn('certificate', result)
        self.assertIn('subject', result['certificate'])
        self.assertIn('issuer', result['certificate'])
        
if __name__ == '__main__':
    unittest.main()
