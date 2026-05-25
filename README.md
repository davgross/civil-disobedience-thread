# Resistance to Civil Government — A Thread

Henry David Thoreau's 1849 essay, rendered as a social media thread and populated with responses from the historical figures his work influenced: Tolstoy, Gandhi, King, Arendt, Buber, Emma Goldman, and many others.

Each paragraph of the essay is a post. Replies, reposts, quote posts, and link cards from the interlocutors are woven in chronologically. Hover any avatar or name to see a profile card.

## Running locally

The page uses `fetch()` to load `data.xml`, which browsers block on `file://` URLs. Serve it with any local HTTP server:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

| File | Role |
|------|------|
| `data.xml` | All content: essay text, authors, replies, likes, quotes, links |
| `index.html` | Minimal HTML shell |
| `style.css` | Layout and visual styling |
| `app.js` | Parses `data.xml` and builds the DOM |
| `generate_avatars.py` | Generates AI portrait avatars via [pollinations.ai](https://pollinations.ai) (free, no API key) |
| `avatars/` | JPEG portraits, one per cast member |

## Adding content

Everything lives in `data.xml`. The basic shapes:

```xml
<!-- A reply from a historical figure -->
<reply id="r42-1" author="tolstoy" timestamp="1894">
  <content>Text, with optional <em>emphasis</em> or <strong>bold</strong>.</content>
  <likes><like author="gandhi"/></likes>
</reply>

<!-- A quote post -->
<quote author="senatorwebster" timestamp="1850" source="Speech in the Senate">
  <content>Quoted text.</content>
</quote>

<!-- A link preview card -->
<link url="https://en.wikipedia.org/wiki/…" title="Article title"
      description="Short excerpt." thumb="https://…/image.jpg"/>
```

See `CLAUDE.md` for the full data model.

## Cast

A growing roster of participants spanning 1780–2008: abolitionists, anarchists, naturalists, novelists, clergy, philosophers, and two bots (WikipediaBot and BibleBot).
