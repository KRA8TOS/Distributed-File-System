import socket
import threading
import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

class MasterNode:
    def __init__(self, host='192.168.246.21', port=5000):  # Laptop 1 IP
        self.metadata = {}
        self.users = {"user1": hashlib.sha256("pass1".encode()).hexdigest()}
        self.tokens = {}
        # Storage Nodes on both laptops
        self.storage_nodes = [" 192.168.246.21:5001", "192.168.246.228:5002"]  # Laptop 1 and Laptop 2
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.next_fd = 0
        print(f"Master Node running on {host}:{port}")

    def encrypt(self, data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt(self, encrypted_data, key):
        data = base64.b64decode(encrypted_data)
        nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def handle_client(self, conn, addr):
        data = conn.recv(1024).decode()
        request = json.loads(data)
        command = request.get("command")
        print(f"DEBUG: Received {command} request: {request}")

        if command == "AUTH":
            username = request.get("username")
            password = request.get("password")
            if self.users.get(username) == hashlib.sha256(password.encode()).hexdigest():
                token = base64.b64encode(get_random_bytes(16)).decode()
                self.tokens[token] = username
                conn.send(json.dumps({"status": "SUCCESS", "token": token}).encode())
            else:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid credentials"}).encode())

        elif command == "OPEN":
            token = request.get("token")
            username = self.tokens.get(token)
            if not username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid token"}).encode())
                return
            filename = request.get("filename")
            mode = request.get("mode")
            if filename not in self.metadata:
                key = get_random_bytes(32)
                self.metadata[filename] = {
                    "nodes": self.storage_nodes,
                    "perms": "rw-r--r--",
                    "owner": username,
                    "key": key,
                    "fd": self.next_fd
                }
                print(f"DEBUG: Created metadata for {filename}: {self.metadata[filename]}")
            if not self.check_perms(filename, username, mode):
                conn.send(json.dumps({"status": "ERROR", "message": "Permission denied"}).encode())
                return
            fd = self.next_fd
            self.metadata[filename]["fd"] = fd
            self.next_fd += 1
            conn.send(json.dumps({"status": "SUCCESS", "fd": fd}).encode())

        elif command == "WRITE":
            token = request.get("token")
            username = self.tokens.get(token)
            if not username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid token"}).encode())
                return
            fd = request.get("fd")
            data = request.get("data")
            filename = next((f for f, meta in self.metadata.items() if meta.get("fd") == fd), None)
            if not filename or self.metadata[filename]["owner"] != username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid FD"}).encode())
                return
            key = self.metadata[filename]["key"]
            encrypted_content = self.encrypt(data, key)
            response = {
                "status": "SUCCESS",
                "nodes": self.metadata[filename]["nodes"],
                "encrypted_content": encrypted_content
            }
            conn.send(json.dumps(response).encode())

        elif command == "READ":
            token = request.get("token")
            username = self.tokens.get(token)
            if not username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid token"}).encode())
                return
            fd = request.get("fd")
            filename = next((f for f, meta in self.metadata.items() if meta.get("fd") == fd), None)
            if not filename or self.metadata[filename]["owner"] != username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid FD"}).encode())
                return
            key = self.metadata[filename]["key"]
            response = {
                "status": "SUCCESS",
                "node": self.metadata[filename]["nodes"][0],
                "key": base64.b64encode(key).decode()
            }
            conn.send(json.dumps(response).encode())

        elif command == "STAT":
            token = request.get("token")
            username = self.tokens.get(token)
            if not username:
                conn.send(json.dumps({"status": "ERROR", "message": "Invalid token"}).encode())
                return
            filename = request.get("filename")
            print(f"DEBUG: STAT check - Filename: {filename}, Metadata: {self.metadata}")
            if filename in self.metadata and self.check_perms(filename, username, "r"):
                info = self.metadata[filename]
                response = {
                    "status": "SUCCESS",
                    "info": f"perms={info['perms']},owner={info['owner']},nodes={','.join(info['nodes'])}"
                }
                conn.send(json.dumps(response).encode())
            else:
                conn.send(json.dumps({"status": "ERROR", "message": "NOT_FOUND"}).encode())

        conn.close()

    def check_perms(self, filename, username, mode):
        perms = self.metadata[filename]["perms"]
        owner = self.metadata[filename]["owner"]
        print(f"DEBUG: Checking perms {perms} for {username} (owner: {owner}) with mode {mode}")
        if username == owner:
            owner_perms = perms[0:3]  # e.g., "rw-"
            if "r" in mode and "r" not in owner_perms:
                return False
            if "w" in mode and "w" not in owner_perms:
                return False
            return True
        else:
            group_perms = perms[3:6]  # e.g., "r--"
            other_perms = perms[6:9]  # e.g., "r--"
            # For simplicity, assume non-owner uses "other" perms
            if "r" in mode and "r" not in other_perms:
                return False
            if "w" in mode and "w" not in other_perms:
                return False
            return True
        return False

    def run(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    master = MasterNode()
    master.run()