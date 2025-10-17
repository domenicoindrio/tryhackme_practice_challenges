"""
hash_cracker.py — Lightweight hash-cracker (dictionary + brute-force)

Purpose: small, educational script used for CTFs / learning.
Usage examples:
    python3 cracker.py -m 0 -a 1 -hs e99a18c428cb38d5f260853678922e03
    python3 cracker.py -m 0 -a 0 --min 1 --max 4 -c ld -hs cfcd208495d565ef66e7dff9f98764da
"""

import argparse
import hashlib
import itertools
import string as s

# Hash algorhitm mapping
algo = {
    0: "md5",
    1: "sha1",
    2: "sha256",
    3: "sha512"
}

# Character set mapping
char_set = {
    "l": s.ascii_letters,
    "d": s.digits,
    "p": s.punctuation,
    "a": s.ascii_letters + s.digits + s.punctuation,
    "t": "abc"
}

def get_char_set(char_input):
    """
    Parses the user input (arg) and returns the 
    respective charachter set chosen (or multiple, if combined)
    """
    comb_charset = ""
    for char in char_input:
        if char in char_set:
            comb_charset += char_set[char]
        else:
            print(f"[-] Invalid charachter set: {char}. Options are: l, d, p, a, t")
    return comb_charset

def string_hash(data, algorithm):
    """
    Hashes a string using the selected algorithm and returns the hex digest.
    Used for comparison with users hash.
    """
    data = data.strip()
    hasher = hashlib.new(algorithm)
    hasher.update(data.encode()) # convert the string into bytes (hashing works on bytes)
    return hasher.hexdigest()

def pwd_gen_from_wordlist(pwd_list_file):
    """
    Generator that yields passwords from a wordlist file.
    """
    try:
        with open(pwd_list_file, "r", encoding="utf-8", errors='ignore') as file:
            for line in file:
                pwd = line.strip()
                yield pwd
    except Exception as e:
        print(f"[-] An error occurred while generating password from the wordlist: \n  > {e}")

def pwd_gen_brute_force(min_len, max_len, charset):
    """
    Generator that yields all possible passwords made from a 
    character set and a specified min and max lenght.
    """
    try:
        for length in range(min_len, max_len + 1):
            for pwd in itertools.product(charset, repeat=length): # this gives back a tuple
                password = ''.join(pwd)  
                yield password
    except Exception as e:
        print(f"[-] An error occurred while generating password: \n  > {e}")

def crack_hash(user_hash, algorithm, pwd_gen):
    """
    It attempts to find the plaintext password of the user's hash by comparing it with 
    generated hashed passwords (using 'algorithm') and checking if equals or not.
    It handles both passwords from a wordlist or brute-force generated.
    """
    try:
        # attempt_counter = 0
        for pwd in pwd_gen:
            # attempt_counter += 1
            # print(f"\rAttempt {attempt_counter}: trying {pwd}", end="", flush=True)
            # print()
            hashed_pwd = string_hash(pwd, algorithm)
            if hashed_pwd == user_hash:
                print(f"[+] Hash cracked! the decoded hash is: {pwd}")
                return True
        else:
            print(f"[-] Cracking of {user_hash} failed")
    except Exception as e:
        print(f"[-] Something went wrong: \n  > {e}")

def cli():
    parser = argparse.ArgumentParser(description="HashMeow, a simple python hashcat-like script")
    parser.add_argument("-m", required=True, type=int, choices=[0, 1, 2, 3], help="Hash mode: `0` (MD5), '1' (SHA-1), '2' (SHA-256), '3' (SHA-512)")
    parser.add_argument("-a", required=True, type=int, choices=[0, 1], help="Attack mode: `0` (Brute-force attack), '1' (Dictionary attack)" )
    parser.add_argument("-pl", "--pwd-list", type=str, default="rockyou.txt", help="Comparison password list. Default is rockyou.txt")

    parser.add_argument("--min", type=int, default=4, help="Min amount of characters for generated password(default=4): Brute-force attack")
    parser.add_argument("--max", type=int, default=10, help="Max amount of characters for generated password(default=10): Brute-force attack")
    parser.add_argument("-c", type=str, default="a", help="Char. set: `l`(letters), `d`(digits)," \
    " `p`(punctuation), `a`(all, default), `t`(test), can be combined, eg. -c ld : Brute-force attack")

    # Mutually exclusive group to require one (and only one) of the given arguments
    # a hash string or a hash file MUST be provided
    # `-h` already reserved for --help
    text_or_file = parser.add_mutually_exclusive_group(required=True)
    text_or_file.add_argument("-hs", type=str, help="Hashstring to crack")
    text_or_file.add_argument("-H", type=str, help="File containing Hashstring/s to crack")

    args = parser.parse_args()
    return args


def main():
    args = cli()
    algorithm = algo.get(args.m)
    char_choice = get_char_set(args.c)
    
    try:
        if args.a == 0:
            pwd_gen = pwd_gen_brute_force(args.min, args.max, char_choice)
            print(f"[*] Brute-force hash generation chosen")
        else: 
            pwd_gen = pwd_gen_from_wordlist(args.pwd_list)
            print(f"[*] Dictionary hash generation chosen")

        if args.hs:
            result = crack_hash(args.hs, algorithm, pwd_gen)
            if result:
                print("[+] Attack completed succesfully, exiting...")
                exit(0)
            else:
                print("[-] Hashing finished without finding the password, exiting...")
                exit(1)        
        elif args.H:
            success = False
            with open(args.H, "r") as f:
                for line in f:
                    line = line.strip()
                    print(f"\n[*] Attempting to crack: {line}")
                    # to prevent pwd generator exhaustion, new generator instance per iterated line
                    if args.a == 0:
                        pwd_gen = pwd_gen_brute_force(args.min, args.max, char_choice)
                    else:
                        pwd_gen = pwd_gen_from_wordlist(args.pwd_list)
                    
                    result = crack_hash(line, algorithm, pwd_gen)
                    if result:
                        success = True
            if success:
                print("[+] At least one hash was cracked successfully, exiting...")
                exit(0)
            else:
                print("[-] Hashing finished without finding the password, exiting...")
                exit(1)          
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user, exiting...")
        exit(0)


if __name__ == "__main__":
    main()
