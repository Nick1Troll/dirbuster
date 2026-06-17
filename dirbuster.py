import argparse
import threading
from queue import Queue
import socket

# --- Argument Definition ---
parser = argparse.ArgumentParser(prog='dirbuster', description='dictionary subdomain enumerator')

parser.add_argument('-w', '--wordlist', action='store', required=True, help='Wordlist for enumeration')
parser.add_argument('-d', '--domain', action='store', required=False, help='Domain to enumerate thru')
parser.add_argument('-th', '--threads', action='store', type=int, default=10, help='Number of worker threads (default: 10)')

args = parser.parse_args()

# --- Eingaben verarbeiten ---
domain = str(args.domain)
world_list_path = args.wordlist
threads = args.threads
ports = [80, 443]

# --- Wordlist einlesen ---
with open(world_list_path, 'r') as f:
    w_list = [line.strip() for line in f]

# --- Domain bereinigen (Protokoll und www entfernen) ---
protocol, m_domain = domain.split(":")
m_domain = m_domain.strip("//").replace("www.", "", 1)

print_lock = threading.Lock()

# --- Verbindungscheck per Socket ---
def single_request(target, port):
    try:
        socket.gethostbyname(target)  # DNS zuerst prüfen
    except socket.gaierror:
        return  # Host existiert nicht, still ignorieren

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            with print_lock:
                print(f"[OPEN] {target}:{port}")

# --- Worker Thread ---
def threader():
    while True:
        target, port = q.get()
        single_request(target, port)
        q.task_done()

# --- Threading Setup ---
q = Queue()

for _ in range(threads):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# --- Queue befüllen ---
for line in w_list:
    dom = line + "." + m_domain
    for port in ports:
        q.put((dom, port))

q.join()