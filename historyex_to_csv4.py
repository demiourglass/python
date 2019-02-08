#!/usr/bin/env python
# import unicodedata

import csv
import datetime
import sqlite3
import time
from sys import argv

outFile = csv.writer(open('historyex.csv', 'w', newline=''), delimiter=' ')

if len(argv) < 2:
    print("Missing historyex.db")
    exit(-1)

component_paths = {}
historyex_types = {'1': 'Create', '2': 'Execute', '4': 'Scan', '6': 'Quarantine', '7': 'Quarantine', '22': 'Move',
                   '40': 'Open'}  # event.h

conn = sqlite3.connect(argv[1])
c_path_history = conn.cursor()
c_component = conn.cursor()

for row in c_path_history.execute("SELECT path, hash, lastref, type FROM path_history ORDER by lastref"):
    str_path = ""
    paths = row[0].split("\\")
    for p in paths:
        if component_paths.get(p) is None:
            for component_name in c_component.execute("SELECT name FROM component WHERE id=? LIMIT 1", (p,)):
                component_paths[p] = component_name[0]

        if str_path == "":
            str_path = "{}".format(component_paths[p])
        elif (p is not None) and (p != "-1"):
            try:
                str_path = "{}\{}".format(str_path, component_paths[p])
            except KeyError:
                str_path = "{}\{}_{}".format(str_path, "MISSING", p)
            except:
                print("ERROR, I don't know what happened?")
    if historyex_types.get(str(row[3])) is None:
        history_ex_type = "UNKNOWN type {}".format(row[3])
    else:
        history_ex_type = historyex_types.get(str(row[3]))

    print("{},{},{},{}".format(str_path, row[1], datetime.datetime.strptime(time.ctime(row[2]), "%a %b %d %H:%M:%S %Y"),
                               history_ex_type))

    outFile.writerow("{},{},{},{}".format(str_path, row[1], datetime.datetime.strptime(time.ctime(row[2]), "%a %b %d %H:%M:%S %Y"),history_ex_type))
