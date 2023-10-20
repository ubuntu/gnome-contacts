#!/usr/bin/env python3

import sys

filename = sys.argv[1]
prefix = sys.argv[2]
if prefix.endswith('/usr'):
    prefix = prefix[:-4]

with open(filename, "r") as pcfile:
    lines = pcfile.readlines()

# remove any prefix entry
newlines = []
for line in lines:
    if line.startswith("prefix="):
        continue
    newlines.append(line)

# add the new prefix
lines = [f'prefix={prefix}\n'] + newlines

# ensure that the specified entries begin with "${prefix}"

newlines = []
for line in lines:
    pos = line.find(f'=/usr')
    if pos != -1:
        if not line[pos+1:].startswith('${prefix}'):
            line = line[:pos+1] + '${prefix}' + line[pos+1:]
    newlines.append(line)
lines = newlines

with open(filename, "w") as pcfile:
    pcfile.writelines(lines)