from OpenSSL import crypto
from pathlib import Path

def generate_self_signed_cert(cert_path, key_path):
    # Generate key
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)
    
    # Generate certificate
    cert = crypto.X509()
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)  # Valid for one year
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    
    # Write certificate and private key to files
    with open(cert_path, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(key_path, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    
    print(f"Generated certificate: {cert_path}")
    print(f"Generated private key: {key_path}")

if __name__ == '__main__':
    cert_path = Path(__file__).parent / 'test_cert.pem'
    key_path = Path(__file__).parent / 'test_key.pem'
    generate_self_signed_cert(cert_path, key_path)
