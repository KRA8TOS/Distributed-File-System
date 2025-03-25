import socket
import json
import base64
from Crypto.Cipher import AES

class ClientNode:
    def __init__(self, master_host='localhost', master_port=5000):
        self.master = (master_host, master_port)
        self.fds = {}  # Maps file descriptors to filenames
        self.token = None

    def login(self, username, password):
        """Authenticate with the Master Node."""
        request = {"command": "AUTH", "username": username, "password": password}
        response = self.send_to_master(request)
        if response.get("status") == "SUCCESS":
            self.token = response.get("token")
            print(f"Logged in as {username}")
        else:
            print("Login failed")

    def open(self, filename, mode):
        """Open a file and get a file descriptor."""
        request = {"command": "OPEN", "token": self.token, "filename": filename, "mode": mode}
        response = self.send_to_master(request)
        if response.get("status") == "SUCCESS":
            fd = response.get("fd")
            self.fds[fd] = filename
            print(f"Opened {filename} with FD: {fd}")
            return fd
        else:
            print(f"Failed to open {filename}: {response.get('message')}")
            return -1

    def write(self, fd, data):
        """Write data to a file using the file descriptor."""
        filename = self.fds.get(fd)
        if not filename:
            print("Invalid FD")
            return
        request = {"command": "WRITE", "token": self.token, "fd": fd, "data": data}
        response = self.send_to_master(request)
        if response.get("status") == "SUCCESS":
            encrypted_content = response.get("encrypted_content")
            nodes = response.get("nodes")
            for node in nodes:
                host, port = node.split(":")
                storage_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                storage_sock.connect((host, int(port)))
                storage_sock.send(f"STORE:{filename}:0:{encrypted_content}".encode())
                storage_sock.recv(1024)  # Acknowledge receipt
                storage_sock.close()
            print("Write successful")
        else:
            print(f"Write failed: {response.get('message')}")

    def read(self, fd):
        """Read data from a file using the file descriptor."""
        filename = self.fds.get(fd)
        if not filename:
            print("Invalid FD")
            return None
        request = {"command": "READ", "token": self.token, "fd": fd}
        response = self.send_to_master(request)
        if response.get("status") == "SUCCESS":
            node = response.get("node")
            key = base64.b64decode(response.get("key"))
            host, port = node.split(":")
            storage_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            storage_sock.connect((host, int(port)))
            storage_sock.send(f"FETCH:{filename}:0:".encode())
            encrypted_content = storage_sock.recv(1024).decode()
            storage_sock.close()
            return self.decrypt(encrypted_content, key)
        else:
            print(f"Read failed: {response.get('message')}")
            return None

    def decrypt(self, encrypted_data, key):
        """Decrypt data retrieved from a Storage Node."""
        data = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def stat(self, filename):
        """Get metadata about a file."""
        request = {"command": "STAT", "token": self.token, "filename": filename}
        response = self.send_to_master(request)
        if response.get("status") == "SUCCESS":
            print(f"Stat for {filename}: {response.get('info')}")
        else:
            print(f"Stat failed: {response.get('message')}")

    def send_to_master(self, request):
        """Send a request to the Master Node and receive a response."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.master)
            sock.send(json.dumps(request).encode())
            response = sock.recv(1024).decode()
            sock.close()
            return json.loads(response)
        except Exception as e:
            print(f"Error communicating with Master Node: {e}")
            return {"status": "ERROR", "message": str(e)}