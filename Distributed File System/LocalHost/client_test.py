from client_node import ClientNode

client = ClientNode()
client.login("user1", "pass1")
while True:
    cmd = input("Enter command (open/write/read/stat/exit): ")
    if cmd == "exit":
        break
    elif cmd == "open":
        filename = input("Filename: ")
        mode = input("Mode (r/w/rw): ")
        fd = client.open(filename, mode)
    elif cmd == "write":
        fd = int(input("FD: "))
        data = input("Data: ")
        client.write(fd, data)
    elif cmd == "read":
        fd = int(input("FD: "))
        print(client.read(fd))
    elif cmd == "stat":
        filename = input("Filename: ")
        client.stat(filename)