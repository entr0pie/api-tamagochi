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

def checkStatus(response, expected_status) -> bool:
    if response.status_code == expected_status:
        print("ok")
        return True 

    print(f"expected {expected_status}, got {response.status_code}")
    return False

print(f"({getTime()}) [INFO] Starting checkup...")

print(f"({getTime()}) [TEST] Checking the / route... ", end="")
checkStatus(get(args.HOST), 200)

print(f"({getTime()}) [TEST] Registering a new parent (davidbowie@email.com:bowiebowie)... ", end="")


print(f"({getTime()}) [TEST] Checking the /parent/login route... ", end="")

