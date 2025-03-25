
## How to Run

Follow these steps to set up and run the Distributed File System on your local machine (Windows, in this case).

### Prerequisites
- **Python 3.x**: Installed on your system (e.g., Python 3.12).
- **Required Library**: Install `pycryptodome` for AES encryption:

```bash
pip install pycryptodome
```

### Steps

#### 1. Clone or Download the Project:
Place all files (`master_node.py`, `storage_node.py`, `client_node.py`, `client_test.py`) in a directory, e.g., `C:\Users\Desktop\Distributed File System`.

#### 2. Start Storage Nodes:
Open two separate PowerShell or Command Prompt windows:

##### Storage Node 1:
```powershell
cd C:\Users\Desktop\Distributed File System
python storage_node.py --host localhost --port 5001 --id storage1
```

##### Storage Node 2:
```powershell
cd C:\Users\Desktop\Distributed File System
python storage_node.py --host localhost --port 5002 --id storage2
```

**Output**: Each node will display `Storage Node [id] running on localhost:[port]`.

#### 3. Start the Master Node:
Open a third terminal window:
```powershell
cd C:\Users\Desktop\Distributed File System
python master_node.py
```

**Output**: `Master Node running on localhost:5000`.

#### 4. Run the Client Test Script:
Open a fourth terminal window:
```powershell
cd C:\Users\Desktop\Distributed File System
python client_test.py
```

**Output**: Expected result:
```text
Logged in as user1
Opened test.txt with FD: 0
Write successful
Single Laptop Test!
Stat for test.txt: perms=rw-r--r--,owner=user1,nodes=localhost:5001,localhost:5002
```

### Notes
- **Order**: Start **Storage Nodes** first, then the **Master Node**, and finally the **Client script**.
- **Stopping**: Press `Ctrl+C` in each terminal to stop the nodes. **Data is lost when nodes shut down** (in-memory storage).

## Dependencies
Ensure you have the following Python libraries installed:
```sh
pip install cryptography
```


