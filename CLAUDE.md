# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static web page displaying Thoreau's "Resistance to Civil Government" as a social media thread, interleaved with responses from historical figures (Tolstoy, Gandhi, MLK, Arendt, etc.) who engaged with his arguments. All participants are treated as contemporaries on the same fictional platform. The full essay (posts p0–p142) is in place, with replies, likes, reposts, and quote posts woven in.

**Avoid brand-specific language** ("Twitter," "tweet," "quote-tweet") in code, comments, commits, and documentation — use "social media thread," "repost," "quote post," etc.

## Architecture

Five files plus supporting assets; no build step, no dependencies.

| File | Role |
|------|------|
| `data.xml` | Single source of truth — all essay text, replies, likes, authors, and thread structure |
| `index.html` | Minimal HTML shell; loads `style.css` and `app.js` |
| `style.css` | Twitter-like layout; CSS variables at top control sizing/colors |
| `app.js` | Fetches and parses `data.xml`, builds DOM, wires interactions |
| `generate_avatars.py` | Generates AI portrait avatars via pollinations.ai (free, no API key) |
| `avatars/` | JPEG avatars, one per cast member (filename = author id) |

### Serving locally

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

`fetch()` is blocked on `file://` URLs, so a local server is required.

---

## Data model (data.xml)

### Authors

```xml
<authors>
  <author id="thoreau">
    <name>Henry David Thoreau</name>
    <handle>hdthoreau</handle>
    <initials>HDT</initials>        <!-- shown when no avatar -->
    <color>#3d6b4f</color>          <!-- avatar background color -->
    <years>1817–1862</years>
    <bio>Short in-character bio — present-tense, as if the author is a contemporary on the platform.</bio>
    <avatar>avatars/thoreau.jpg</avatar>   <!-- optional -->
  </author>
</authors>
```

### Posts and thread elements

```xml
<posts>
  <post id="p1" author="thoreau" timestamp="1849">
    <content>Essay text, may contain <em>emphasis</em> or <strong>bold</strong>.</content>

    <!-- Optional quote post box (rendered below content) -->
    <quote author="senatorwebster" timestamp="1850" source="Speech in the Senate">
      <content>Quoted text, also supports <em>em</em>/<strong>strong</strong>/<br/>.</content>
    </quote>
    <!-- OR for non-cast people: -->
    <quote name="Display Name" timestamp="1850" source="Source title">
      <content>…</content>
    </quote>

    <!-- Optional link preview card -->
    <link url="https://en.wikipedia.org/wiki/Powder_monkey"
          title="Powder monkey"
          description="Brief excerpt shown below the title."
          thumb="https://upload.wikimedia.org/…/320px-filename.jpg"/>
    <!-- thumb is optional; card degrades gracefully without it -->

    <likes>
      <like author="gandhi"/>
    </likes>
    <!-- Bare <like author="id"/> directly on an element also works -->

    <replies>
      <reply id="r1-1" author="tolstoy" timestamp="1894">
        <content>…</content>
        <likes>…</likes>
        <replies>           <!-- nesting supported to any depth -->
          <reply id="r1-1-1" author="king" timestamp="1963">…</reply>
        </replies>
      </reply>

      <repost id="rp1-1" author="alcott" timestamp="1848">
        <content>Optional comment text shown above the repost label.</content>
      </repost>
    </replies>
  </post>
</posts>
```

All six child element types (`content`, `quote`, `link`, `likes`, `replies`, `repost`) are optional on any given post or reply.

### ID conventions

- Posts: `p0`, `p1`, … `p142` (sequential, no gaps)
- Replies: `r{post}-{n}`, e.g. `r1-1`, `r1-2`; nested: `r1-1-1`
- Reposts: `rp{post}-{n}`, e.g. `rp1-1`

### Inline markup inside `<content>`

`<em>`, `<strong>`, and `<br/>` are supported and rendered faithfully. Plain `&amp;`, `&lt;` etc. for literal characters. Use straight ASCII double-quotes for all XML attribute values — curly/smart quotes in attributes break the parser. Also avoid plain ASCII apostrophes (`'`) inside attribute values (e.g. in `description=`): use `&apos;` or a curly apostrophe (`’`) instead, as a bare `'` can confuse the browser's XML parser.

---

## Cast members

Authors currently in data.xml (id → display name):

| id | Name |
|----|------|
| `thoreau` | Henry David Thoreau |
| `alcott` | Amos Bronson Alcott |
| `amalcott` | Abby May Alcott |
| `emerson` | Ralph Waldo Emerson |
| `hgoblake` | H.G.O. Blake |
| `tolstoy` | Leo Tolstoy |
| `gandhi` | Mohandas K. Gandhi |
| `king` | Martin Luther King Jr. |
| `arendt` | Hannah Arendt |
| `debs` | Eugene V. Debs |
| `hennacy` | Ammon Hennacy |
| `redemma` | Emma Goldman |
| `senatorwebster` | Daniel Webster |
| `george_peele` | George Peele |
| `williampaley` | William Paley |
| `thebard` | William Shakespeare |
| `thomas_middleton` | Thomas Middleton |
| `charleswolfe` | Charles Wolfe |
| `kongqiu` | Confucius |
| `tusitala` | Robert Louis Stevenson |
| `JamesMacKaye` | James MacKaye |
| `larosenwa` | Larry Rosenwald |
| `anonym` | Anon. (Danish resistance) |
| `biblebot` | BibleBot |
| `wikibot` | WikipediaBot |
| `TerenceBall` | Terence Ball |
| `JamesFChildress` | James F. Childress |
| `CurtisCrawford` | Curtis Crawford |
| `NormanJacobson` | Norman Jacobson |

`wikibot` has no avatar (initials only); all others have JPEGs in `avatars/`.

### Adding a new author

1. Add `<author id="…">` entry in `data.xml`
2. Add an entry in `generate_avatars.py` SUBJECTS list with a descriptive prompt and unique seed
3. Run `python3 generate_avatars.py` (skips already-generated files)

---

## app.js structure

Key functions:

| Function | Purpose |
|----------|---------|
| `buildPost(postEl, isLast)` | Top-level post wrapper + thread line |
| `buildThreadItem(itemEl, depth)` | Dispatcher: routes `<reply>` or `<repost>` |
| `buildReplyRow(replyEl, depth)` | Indented reply; recurses for children |
| `buildRepostRow(repostEl, depth)` | Repost row with ↻ header |
| `buildBody(xmlEl, author, ts, threadItems, bodyClass)` | Content column shared by posts and replies |
| `buildQuoteBox(quoteEl)` | Quote-tweet box |
| `buildLinkCard(linkEl)` | External link preview card |
| `buildAvatar(author, size)` | Avatar circle (image or initials fallback) |
| `getContentHtml(xmlEl)` | Serializes `<content>` preserving `<em>`/`<strong>`/`<br>` |
| `getLikeEls(el)` | Returns like elements from both `<likes><like/>` and bare `<like/>` patterns |

Depth-based indentation: `replyPad(depth) = 28 + depth × 24` px.

---

## Utilities

- `wrap_posts.py` — one-time script used to wrap plaintext paragraphs into `<post>` elements
- `renumber_posts.py` — renumbers post IDs to close gaps after structural edits
