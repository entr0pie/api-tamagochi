#!/bin/python3

from argparse import ArgumentParser
from requests import get, post

parser = ArgumentParser(prog="checkup.py",
                        description="Check the status of Tamagochi API",
                        epilog="See https://github.com/entr0pie/api-tamagochi for more information.")

parser.add_argument("HOST", type=str, help="The base address of Tamagochi API")
parser.add_argument("--verbose", "-v", required=False, action='store_true', help="Verbose mode")
args = parser.parse_args()

class Colors:
    def __init__(self):
        self.info = "\u001b[36m"
        self.success = "\u001b[32;1m"
        self.warn = "\u001b[33;1m"
        self.error = "\u001b[31;1m"
        self.reset = "\u001b[0m"

c = Colors()

verbose = lambda content: print(f"(VERB) {content}") if args.verbose else None
status_check = lambda expected, given: print(f"{c.success}ok!{c.reset}") if expected == given else print(f"{c.warn}expected {expected}, given {given}{c.reset}")

verbose("Starting the script")

print("(TEST) Testing the main route... ", end="")
response = get(args.HOST)
status_check(200, response.status_code)




