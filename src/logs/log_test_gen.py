import os
import random
from datetime import datetime, timedelta

# Define o diretório onde os logs serão guardados
LOG_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_ssh_logs(filename="dummy_ssh.log", lines=50):
    filepath = os.path.join(LOG_DIR, filename)
    ips = ["192.168.1.15", "10.0.0.5", "116.31.116.5", "45.33.32.156", "185.70.1.1"]
    users = ["root", "admin", "user", "guest"]
    
    with open(filepath, "w") as f:
        for _ in range(lines):
            date = (datetime.now() - timedelta(minutes=random.randint(1, 1200))).strftime("%b %d %H:%M:%S")
            ip = random.choice(ips)
            user = random.choice(users)
            
            if random.choice([True, False]):
                msg = f"Failed password for {user} from {ip} port {random.randint(1024,65535)} ssh2"
            else:
                msg = f"Accepted password for {user} from {ip} port {random.randint(1024,65535)} ssh2"
                
            f.write(f"{date} server-lpd sshd[{random.randint(1000,9999)}]: {msg}\n")
    print(f"[+] Gerado log SSH: {filename}")

def generate_http_logs(filename="dummy_http.log", lines=50):
    filepath = os.path.join(LOG_DIR, filename)
    ips = ["1.1.1.1", "2.2.2.2", "192.168.1.50"]
    
    with open(filepath, "w") as f:
        for _ in range(lines):
            date = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
            ip = random.choice(ips)
            status = random.choice(["200", "404", "500"])
            f.write(f'{ip} - - [{date}] "GET /index.html HTTP/1.1" {status} 1024\n')
    print(f"[+] Gerado log HTTP: {filename}")

if __name__ == "__main__":
    generate_ssh_logs()
    generate_http_logs()