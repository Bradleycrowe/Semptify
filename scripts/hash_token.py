import hashlib
import sys


def hash_token(token: str) -> str:
    return 'sha256:' + hashlib.sha256(token.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python scripts/hash_token.py <plain_token>')
        sys.exit(1)
    print(hash_token(sys.argv[1]))
