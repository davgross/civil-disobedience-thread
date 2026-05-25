#!/usr/bin/env python3
"""
Wrap the plaintext paragraphs in data.xml (after p13) into <post> elements.
Each blank-line-separated block becomes one post (p14, p15, ...).
The <em>/<strong> tags already present in the text are preserved as-is.
"""
import re, sys

with open('data.xml', 'r', encoding='utf-8') as f:
    content = f.read()

p13_start = content.find('<post id="p13"')
if p13_start == -1:
    sys.exit("Can't find p13")

p13_close = content.find('</post>', p13_start)
if p13_close == -1:
    sys.exit("Can't find end of p13")

after_p13 = p13_close + len('</post>')

posts_close = content.find('</posts>', after_p13)
if posts_close == -1:
    sys.exit("Can't find </posts>")

plaintext = content[after_p13:posts_close]

# Strip XML comments
plaintext = re.sub(r'<!--.*?-->', '', plaintext, flags=re.DOTALL)

# Split into paragraphs on blank lines
paragraphs = []
current = []
for line in plaintext.split('\n'):
    stripped = line.strip()
    if stripped:
        current.append(stripped)
    else:
        if current:
            paragraphs.append(' '.join(current))
            current = []
if current:
    paragraphs.append(' '.join(current))

new_posts = []
for i, para in enumerate(paragraphs):
    pid = f'p{14 + i}'
    new_posts.append(
        f'    <post id="{pid}" author="thoreau" timestamp="1849">\n'
        f'      <content>{para}</content>\n'
        f'      <likes/>\n'
        f'      <replies/>\n'
        f'    </post>'
    )

new_section = '\n\n' + '\n\n'.join(new_posts) + '\n\n  '

result = content[:after_p13] + new_section + '</posts>' + content[posts_close + len('</posts>'):]

with open('data.xml', 'w', encoding='utf-8') as f:
    f.write(result)

print(f"Wrapped {len(paragraphs)} paragraphs as posts p14–p{13 + len(paragraphs)}")
