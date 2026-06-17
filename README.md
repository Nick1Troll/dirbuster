# Dirbuster

A multithreaded subdomain enumerator written in Python, inspired by Gobuster. Built as a learning project as part of 100 Days of Code.

## Features

- Enumerates subdomains via wordlist
- Multithreaded with configurable thread count (queue worker pattern)
- DNS resolution check before connection attempt
- Checks ports 80 and 443 per subdomain
- Clean output, only open hosts are printed

## Requirements

- Python 3.8+
- No external dependencies, standard library only

## Installation

```bash
git clone git@github.com:Nick1Troll/dirbuster.git
cd dirbuster
```

## Usage

```bash
python dirbuster.py -w <wordlist> -d <domain> [-th <threads>]
```

### Arguments

| Flag | Long | Description | Required |
|------|------|-------------|----------|
| `-w` | `--wordlist` | Path to wordlist file | Yes |
| `-d` | `--domain` | Target domain (e.g. `https://www.example.com/`) | Yes |
| `-th` | `--threads` | Number of worker threads (default: 10) | No |

## Examples

**Basic scan:**
```bash
python dirbuster.py -w wordlist.txt -d https://www.example.com/
```

**More threads for faster scanning:**
```bash
python dirbuster.py -w wordlist.txt -d https://www.example.com/ -th 50
```

### Example Output
[OPEN] api.example.com:80
[OPEN] mail.example.com:443

## Legal Notice

This tool is intended for use on domains you own or have explicit permission to test. Subdomain enumeration on third-party systems without authorization may be illegal. Use responsibly.

## Technical Notes

- **Socket:** `connect_ex()` for clean error handling without exceptions
- **DNS:** `gethostbyname()` validates host existence before connection attempt
- **Threading:** Queue worker pattern with daemon threads
- **Lock:** `threading.Lock()` protects console output from race conditions