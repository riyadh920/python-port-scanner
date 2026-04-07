import socket
import threading
from queue import Queue

target = input("Enter target IP: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(f"\nScanning target {target}...\n")

queue = Queue()
open_ports = []

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        
        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "No banner"
                
            print(f"[OPEN] Port {port} | {banner}")
            open_ports.append(port)
            
            with open("results.txt", "a") as f:
                f.write(f"Port {port} is open | {banner}\n")
                
        s.close()
    except:
        pass

def threader():
    while True:
        port = queue.get()
        scan_port(port)
        queue.task_done()

for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for port in range(start_port, end_port + 1):
    queue.put(port)

queue.join()

print("\nScan completed!")
print("Open ports:", open_ports)
