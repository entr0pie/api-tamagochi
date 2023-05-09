from argparse import ArgumentParser

import sqlite3

parser = ArgumentParser(prog="create_db", 
                        description="Create a SQLite DB from a file")

parser.add_argument("FILE", type=str, help="file to use", dest="file")
parser.add_argument("-o", "--output", type=str, help="output .db file", dest="output")
args = parser.parse_args()

conn = sqlite3.connect(args.file)
cursor = conn.cursor()

with open(args.output, 'r') as f:
    sql = f.read()

cursor.executescript(sql)

conn.commit()
conn.close()