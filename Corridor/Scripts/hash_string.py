"""
hash_string.py — simple string hasher

Usage examples:
    python3 hash_string.py -s "hello" -a md5
    python3 hash_string.py -s "0" -a md5
"""
import hashlib, argparse, sys

def hash_string(string, algorithm):
    if algorithm not in hashlib.algorithms_guaranteed:
        raise ValueError(f"'{algorithm}' is not supported.")
    hasher = hashlib.new(algorithm)
    hasher.update(string.encode("utf-8"))
    return hasher.hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Simple python strings hasher")
    parser.add_argument("-s", "--string", required=True, help="String to hash (if it contains spaces or special chars, wrap it in quotes)")
    parser.add_argument("-a", "--algorithm", required=True, help="Hash algorithm")

    args = parser.parse_args()

    try:
        hash_value = hash_string(args.string, args.algorithm)
        print(f"Here the hash value for <{args.string}> using {args.algorithm} algorithm: \n{hash_value}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()