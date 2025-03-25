# Distributed File System (DFS)

## Project Overview
This project implements a Distributed File System (DFS) in Python, designed to simulate a decentralized storage solution. It allows users to store, retrieve, and manage files across multiple nodes with encryption for security. The system consists of a Master Node for metadata management and coordination, Storage Nodes for holding encrypted file content in memory, and a Client Node for user interaction. 

Master Node: Manages metadata and coordinates nodes.

Storage Nodes: Store encrypted file content in memory.

Client Node: Provides user interaction for file operations.

### Key Features
- **Authentication**: Token-based user login.
- **File Operations**: Open, write, read, and stat (metadata retrieval).
- **Encryption**: AES encryption for data security.
- **In-Memory Storage**: Data persists in memory during runtime.

This project serves as a proof-of-concept for distributed systems, demonstrating concepts like **node coordination, data replication, and secure communication**.

## Files
The project consists of four main Python scripts:

### 1. `master_node.py`
- **Purpose**: Acts as the central coordinator.
- **Functionality**: Manages file metadata (permissions, ownership, encryption keys), authenticates users, and directs Storage Nodes.
- **Key Components**: Metadata dictionary, token generation, AES encryption/decryption.

### 2. `storage_node.py`
- **Purpose**: Stores encrypted file content.
- **Functionality**: Receives and serves data via socket communication, maintaining an in-memory storage dictionary.
- **Key Components**: Socket server, `self.storage` for data.

### 3. `client_node.py`
- **Purpose**: Provides the user interface to interact with the system.
- **Functionality**: Handles login, file operations (open, write, read, stat), and communicates with Master and Storage Nodes.
- **Key Components**: `ClientNode` class, socket communication, decryption.

### 4. `client_test.py`
- **Purpose**: Test script to demonstrate system functionality.
- **Functionality**: Executes a sequence of operations (login, open, write, read, stat) to verify the system works.
- **Key Components**: Simple script calling `ClientNode` methods.

## How to Run
1. Start the **Master Node**:
   ```sh
   python master_node.py
   ```
2. Start one or more **Storage Nodes**:
   ```sh
   python storage_node.py
   ```
3. Run the **Client Node** to interact with the system:
   ```sh
   python client_node.py
   ```
4. (Optional) Run the test script:
   ```sh
   python client_test.py
   ```

## Dependencies
Ensure you have the following Python libraries installed:
```sh
pip install cryptography
```

## Future Enhancements
- **Persistent Storage**: Implement file persistence beyond runtime.
- **Data Replication**: Improve fault tolerance by duplicating stored data.
- **Advanced Authentication**: Enhance security with multi-factor authentication.

## License
This project is licensed under the MIT License.

---
Feel free to contribute and enhance this project!

