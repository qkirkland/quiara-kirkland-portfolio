import sys
import socket
import ssl
import os

CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'

# Generate self-signed cert if not present (for demo only)
def ensure_cert():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print('[*] Generating self-signed certificate...')
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        import datetime
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'PA'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'Philadelphia'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Quiara Kirkland'),
            x509.NameAttribute(NameOID.COMMON_NAME, u'localhost'),
        ])
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
            key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.datetime.utcnow()).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)).sign(key, hashes.SHA256())
        with open(CERT_FILE, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        with open(KEY_FILE, 'wb') as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

def send_file(file_path, host, port):
    ensure_cert()
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            with open(file_path, 'rb') as f:
                data = f.read()
                ssock.sendall(len(data).to_bytes(8, 'big'))
                ssock.sendall(data)
            print(f'[+] Sent {file_path} to {host}:{port}')

def receive_file(port):
    ensure_cert()
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind(('0.0.0.0', port))
        sock.listen(1)
        print(f'[*] Listening on port {port}...')
        conn, addr = sock.accept()
        with context.wrap_socket(conn, server_side=True) as ssock:
            print(f'[+] Connection from {addr}')
            size = int.from_bytes(ssock.recv(8), 'big')
            data = b''
            while len(data) < size:
                chunk = ssock.recv(min(4096, size - len(data)))
                if not chunk:
                    break
                data += chunk
            out_file = 'received_file'
            with open(out_file, 'wb') as f:
                f.write(data)
            print(f'[+] Received file saved as {out_file}')

def main():
    if len(sys.argv) < 2:
        print("Usage: python secure_file_transfer.py send <file> <host> <port> | receive <port>")
        return
    mode = sys.argv[1]
    if mode == "send" and len(sys.argv) == 5:
        send_file(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif mode == "receive" and len(sys.argv) == 3:
        receive_file(int(sys.argv[2]))
    else:
        print("Invalid arguments.")

if __name__ == "__main__":
    main() 