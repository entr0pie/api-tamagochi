#!/bin/python3

from argparse import ArgumentParser
from requests import get, post

parser = ArgumentParser(prog="checkup.py",
                        description="Check the status of Tamagochi API",
                        epilog="See https://github.com/entr0pie/api-tamagochi for more information.")

parser.add_argument("HOST", type=str, help="The base address of Tamagochi API")
parser.add_argument("--verbose", "-v", required=False, action='store_true', help="Verbose mode")
args = parser.parse_args()


