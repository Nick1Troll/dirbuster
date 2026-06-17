import argparse
import threading
from queue import Queue
import socket

# --- Argument Definition ---
parser = argparse.ArgumentParser(prog='subbuster', description='dictionary subdomain enumerator')

parser.add_argument('-w', '--wordlist', action='store', required=True, help='Wordlist for enumeration')
parser.add_argument('-d', '--domain', action='store', required=True, help='Domain to enumerate (e.g. example.com or https://www.example.com/)')
parser.add_argument('-th', '--threads', action='store', type=int, default=10, help='Number of worker threads (default: 10)')

args = parser.parse_args()

# --- Eingaben verarbeiten ---
world_list_path = args.wordlist
threads = args.threads
ports = [80, 443]


# --- Domain bereinigen (Protokoll, www, Pfad und Port entfernen) ---
def clean_domain(raw):
    raw = raw.strip()
    # Schema entfernen, falls vorhanden (https://, http://)
    if "://" in raw:
        raw = raw.split("://", 1)[1]
    # Pfad entfernen (alles ab dem ersten /)
    raw = raw.split("/", 1)[0]
    # Port entfernen, falls angegeben (example.com:8080)
    raw = raw.split(":", 1)[0]
    # führendes www. entfernen
    if raw.startswith("www."):
        raw = raw[4:]
    return raw


m_domain = clean_domain(args.domain)

# --- Wordlist einlesen ---
with open(world_list_path, 'r') as f:
    w_list = [line.strip() for line in f]

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