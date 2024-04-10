#!/usr/bin/python3

import requests
import sys
import argparse
import threading
from pyfiglet import Figlet

# Colours for UI
YELLOW = '\u001b[1;93m'
CYN = '\u001b[1;96m'
RED = '\u001b[1;91m'
GRN = '\u001b[1;92m'
WHITE = '\u001b[1;37m'
BLACK = '\u001b[1;30m'
negative_status_codes = [400, 404, 401, 403]


def check_directory(url, wordlist, codes, hits, lock, verbose=False):
    total_words = len(wordlist)
    for idx, word in enumerate(wordlist):
        try:
            response = requests.get(f"{url}/{word}", timeout=5)

            if response.status_code not in negative_status_codes:
                with lock:
                    print(
                        f"\r{CYN}Progress:{GRN} [{'+'}] Found: {WHITE}/{word} [{response.status_code}]{' ' * (50 - len(word))} Checked {idx + 1}/{total_words} words".ljust(
                            100), flush=True, end='\n')
        except requests.RequestException as e:
            if verbose:
                with lock:
                    print(f"\r{CYN}Progress:{WHITE} [{'!'}] Error: {e}", flush=True)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt: Stopping the directory enumeration process...")
            sys.exit(0)  # Exit the script with status code 0 (indicating clean exit)


def main():
    # Arguments
    parser = argparse.ArgumentParser(
        description="usage: BAAS.py [-h] -u URL -w WORDLIST [--status STATUS [STATUS ...]] [--install] [-t THREAD] options:")
    parser.add_argument("-u", "--url", metavar="URL", required=True, help="Target URL (e.g., http://example.com).")
    parser.add_argument("-w", "--wordlist", metavar="WORDLIST", required=True, help="Path to the wordlist file.")
    parser.add_argument("--status", dest="status", nargs='+', type=int, default=[404], metavar="STATUS",
                        help="Negative status codes to exclude.")
    parser.add_argument("-t", "--threads", metavar="THREAD", type=int, default=100,
                        help="Number of threads to use for scanning.")
    args = parser.parse_args()

    # BAAS logo
    f = Figlet(font='slant')
    baas_text = f.renderText('BAAS')
    print(baas_text)
    print(
        f"{CYN}BAAS is a directory enumeration tool designed for penetration testers and security researchers.{WHITE}")

    target_url = args.url
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        print(
            f"{CYN}[{RED}!{CYN}]{WHITE} Incorrect URL: {target_url}\n{CYN}[{RED}!{CYN}]{WHITE} URL should start with 'http://' or 'https://'.")
        sys.exit(1)

    wordlist_file = args.wordlist
    num_threads = args.threads
    hits = []
    lock = threading.Lock()

    print("=" * 101)
    print(f"{BLACK}Created by @baas on twitter{WHITE}")
    print(f"[+] URL:                     {target_url}")
    print(f"[+] Threads:                 {num_threads}")
    print(f"[+] Wordlist:                {wordlist_file}")
    print(f"[+] Negative Status codes:   {negative_status_codes}")
    print("=" * 101)

    try:
        with open(wordlist_file, 'r') as f:
            wordlist = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"{CYN}[{RED}!{CYN}]{WHITE} Wordlist file not found.")
        sys.exit(1)

    check_directory(target_url, wordlist, negative_status_codes, hits, lock)

    print(f"\n{CYN}[{GRN}*{CYN}]{WHITE} Finished. Total {len(hits)} directories found.")


if __name__ == "__main__":
    main()
