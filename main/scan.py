import time
import socket

from abc import ABC, abstractmethod

class scanner(ABC):
    def __init__(self, targets):
        self.targets = targets

    @abstractmethod
    def scan(self): ...
    
class assesmentManager(scanner):
    def __init__ (self, targets, port):
        super().__init__(targets)
        self.start_vuln_scan = vulnerabilityScanner(targets)
        self.start_port_scan = portScanner(targets, port)

    def scan(self):
        print(f"scanning port targets: {self.targets}")
        self.start_vuln_scan.scan()
        self.start_port_scan.scan()

    def report_gen():
        print("reports generated")
    
class vulnerabilityScanner(scanner):
    def __init__(self, targets):
        super().__init__(targets)

    def scan(self):
        for i in self.targets:
            print(f"initiating vulnerability scan: {i}")
        time.sleep(5) #place holder for actual implementation
        print("vulnerability scan done")
        

class portScanner(scanner):
    def __init__(self, targets, port):
        super().__init__(targets)
        self.port = port

    def scan(self):

        print("running port scan...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            if s.connect_ex((self.targets,self.port)) == 0:
                try:
                    banner = s.recv(1024).decode(errors = "ignore").strip()
                    print(f"[SUCCESS] {banner}")
                except socket.timeout:
                    print("[ERROR] dint work")
                print(f"[OPEN] {self.targets}:{self.port} -> {banner}")

        print("here 1")
        
assesment1 = assesmentManager("127.0.0.1", 8080)
assesment1.scan()
