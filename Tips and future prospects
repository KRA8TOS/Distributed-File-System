# Performing Operations

## Custom Operations
To perform custom operations, edit `client_test.py`:

1. Open `client_test.py` in a text editor.
2. Add operations, for example:

```python
from client_node import ClientNode

client = ClientNode()
client.login("user1", "pass1")
fd = client.open("myfile.txt", "rw")
if fd != -1:
    client.write(fd, "Custom data here!")
    print(client.read(fd))
    client.stat("myfile.txt")
```

3. Run the script:

```bash
python client_test.py
```

### Output Location
- Results (e.g., read data, stat info) appear in the terminal where you run `client_test.py`.

## Where Data is Stored
- **In-Memory**: Data is stored in the `self.storage` dictionary of each `StorageNode` instance (e.g., `localhost:5001` and `localhost:5002`) as encrypted strings.
- **Viewing Data**: Use `client.read(fd)` in `client_test.py` to fetch and display decrypted data, or modify `storage_node.py` to print `self.storage` contents (see debugging tips below).
- **Persistence**: Currently non-persistent; data is lost when Storage Nodes stop.

## Future Prospects
This project can be extended in several ways to enhance functionality and real-world applicability:

### Persistent Storage
Modify `storage_node.py` to save encrypted data to disk:

```python
def handle_client(self, conn, addr):
    data = conn.recv(1024).decode()
    parts = data.split(":", 3)
    command, filename = parts[0], parts[1]
    if command == "STORE":
        encrypted_content = parts[3]
        with open(f"{filename}.enc", "w") as f:
            f.write(encrypted_content)
        conn.send("STORED".encode())
    elif command == "FETCH":
        try:
            with open(f"{filename}.enc", "r") as f:
                content = f.read()
            conn.send(content.encode())
        except FileNotFoundError:
            conn.send("NOT_FOUND".encode())
    conn.close()
```

This would store files like `test.txt.enc` on disk, surviving restarts.

### Command-Line Interface (CLI)
Add an interactive CLI to `client_test.py`:

```python
while True:
    cmd = input("Command (open/write/read/stat/exit): ")
    if cmd == "exit":
        break
    # Add logic for each command
```

Allows dynamic user interaction.

### Replication and Fault Tolerance
- Implement data replication across Storage Nodes with consistency checks.
- Add failover if a Storage Node goes down.

### User Management
- Extend `master_node.py` to support multiple users with a user database instead of hardcoded credentials.

### GUI
- Develop a graphical interface using **Tkinter** or **Flask** for easier file management.

### Performance Optimization
- Use asynchronous I/O (e.g., `asyncio`) for better scalability.
- Compress data before encryption to reduce storage and transfer overhead.

## Debugging Tips
### See Stored Data
Add prints in `storage_node.py`:

```python
if command == "STORE":
    encrypted_content = parts[3]
    self.storage[filename] = encrypted_content
    print(f"Stored {filename}: {encrypted_content[:20]}...")
```

### Check Metadata
- View Master Node logs in its terminal for DEBUG messages.

### Errors
- If an operation fails, check all terminal outputs for error messages.

## About This Project
This **Distributed File System** is an educational tool and prototype for learning distributed systems concepts:

- **Purpose**: Demonstrate client-server architecture, encryption, and node coordination.
- **Use Case**: Ideal for experimenting with distributed storage ideas or as a starting point for more complex systems.
- **Limitations**: In-memory storage, single-user focus, and basic error handling make it unsuitable for production without enhancements.

**Feel free to contribute or adapt this project for your needs!**

