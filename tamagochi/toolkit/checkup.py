#!/bin/python3

from datetime import datetime 
from argparse import ArgumentParser

from requests import get, post

parser = ArgumentParser(prog="checkup.py",
                        description="Check the status of Tamagochi API",
                        epilog="See https://github.com/entr0pie/api-tamagochi for more information.")

parser.add_argument("HOST", type=str, help="The base address of Tamagochi API")
parser.add_argument("--verbose", "-v", required=False, action='store_true', help="Verbose mode")
args = parser.parse_args()

verbose = lambda message: print(f"[VERBOSE] {message}") if args.verbose else None
getTime = lambda: datetime.now().strftime("%H:%M:%S")

def checkStatus(expected: int, received: int) -> bool:
    if expected == received:
        print("\u001b[32;1mok\u001b[0m")
        return True

    print(f"expected {expected}, got \u001b[33;1m{received}.\u001b[0m")
    return False

print(f"({getTime()}) [INFO] Starting checkup...")

print(f"({getTime()}) [PARENT] Registering a new account (test@email@.com:password) ... ", end="")
register_data = {
    "name":"Name",
    "surname":"Surname",
    "email":"test@email.com",
    "password":"password",
    "gender":"m"
}

response = post(f"{args.HOST}/parent/register", json=register_data)
checkStatus(200, response.status_code)

print(f"({getTime()}) [PARENT] Login in... ", end="")
login_data = {
    "email":"test@email.com",
    "password":"password"
}

response = post(f"{args.HOST}/parent/login", json=login_data)
checkStatus(200, response.status_code)

auth_header = response.json()['access_token']

print(f"({getTime()}) [TEST] Checking the /parent/private route... ", end="")
response = get(f"{args.HOST}/parent/protected", headers={"Authorization": f"Bearer {auth_header}"})
print(response.content)

