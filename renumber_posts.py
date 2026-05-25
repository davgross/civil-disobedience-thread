#!/usr/bin/env python3
"""
Close two gaps in post IDs:
  - p125 is missing: shift p126-p135 down by 1
  - p136 is missing: shift p137-p144 down by 2 (cumulative)
"""
import re

with open('data.xml', 'r', encoding='utf-8') as f:
    content = f.read()

mapping = {}
for n in range(126, 136):   # gap at p125: shift 1
    mapping[n] = n - 1
for n in range(137, 145):   # gap at p136 (after first shift): shift 2
    mapping[n] = n - 2

# Work in descending order to avoid p126→p125 then p125 being touched again
for old_n in sorted(mapping.keys(), reverse=True):
    new_n = mapping[old_n]
    content = content.replace(f'id="p{old_n}"', f'id="p{new_n}"')
    content = re.sub(rf'id="r{old_n}-', f'id="r{new_n}-', content)

with open('data.xml', 'w', encoding='utf-8') as f:
    f.write(content)

for old_n in sorted(mapping.keys()):
    print(f"  p{old_n} → p{mapping[old_n]}")
