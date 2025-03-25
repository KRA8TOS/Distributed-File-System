import socket
import threading
import argparse

class StorageNode:
    def __init__(self, host='localhost', port=5001, node_id="storage1"):
        self.storage = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Storage Node {node_id} running on {host}:{port}")

    def handle_client(self, conn, addr):
        data = conn.recv(1024).decode()
        parts = data.split(":", 3)
        command, filename = parts[0], parts[1]
        if command == "STORE":
            encrypted_content = parts[3]
            self.storage[filename] = encrypted_content
            print(f"Stored {filename}: {encrypted_content[:20]}... (length: {len(encrypted_content)})")
            conn.send("STORED".encode())
        elif command == "FETCH":
            content = self.storage.get(filename, "NOT_FOUND")
            print(f"Fetching {filename}: {content[:20]}... (length: {len(content)})")
            conn.send(content.encode())
        conn.close()

    def run(self):
        while True:
            conn, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Storage Node")
    parser.add_argument("--host", default="localhost", help="Host address")
    parser.add_argument("--port", type=int, default=5001, help="Port number")
    parser.add_argument("--id", default="storage1", help="Node ID")
    args = parser.parse_args()
    
    storage = StorageNode(host=args.host, port=args.port, node_id=args.id)
    storage.run()