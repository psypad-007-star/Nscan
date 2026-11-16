import time

from abc import ABC, abstractmethod

class scanner(ABC):
    def __init__(self, target):
        self.target = target

    @abstractmethod
    def scan(self):
        pass
    
class assesmentManager(scanner):
    def __init__ (self, target, port):
        super().__init__(target)
        self.start_vuln_scan = vulnerabilityScanner(target)
        self.start_port_scan = portScanner(target, port)

    def scan(self):
        print(f"scanning port Target: {self.target}")
        self.start_vuln_scan.scan()
        self.start_port_scan.scan()

    def report_gen():
        print("reports generated")
    
class vulnerabilityScanner(scanner):
    def __init__(self, target):
        super().__init__(target)

    def scan(self):
        print(f"initiating vulnerability scan: {self.target}")
        time.sleep(5) #place holder for actual implementation
        print("vulnerability scan done")
        

class portScanner(scanner):
    def __init__(self, target, port):
        super().__init__(target)
        self.port = port

    def scan(self):

        print("running port scan...")

        while True:
            time.sleep(5) #place holder for true implementation
            print("scan done")
            break



assesment1 = assesmentManager("192.168.13.22", 22)
assesment1.scan()
