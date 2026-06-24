/* app.js — parses data.xml and renders the thread UI */
'use strict';

(async () => {
  const container = document.getElementById('thread-container');
  const tooltip   = document.getElementById('profile-tooltip');

  let authors = {};

  // ── Load & parse data.xml ──────────────────────────────────────────
  let doc;
  try {
    const resp = await fetch('data.xml');
    if (!resp.ok) throw new Error(`HTTP ${resp.status} fetching data.xml`);
    const xml = await resp.text();
    doc = new DOMParser().parseFromString(xml, 'application/xml');
    const err = doc.querySelector('parsererror');
    if (err) throw new Error('XML parse error: ' + err.textContent.slice(0, 120));
  } catch (e) {
    container.innerHTML =
      `<div class="error-msg">
        <strong>Could not load thread data.</strong><br>${escHtml(e.message)}<br><br>
        Run a local server to avoid CORS restrictions:<br>
        <code>python3 -m http.server 8000</code>
        &nbsp;then open&nbsp;<code>http://localhost:8000</code>
      </div>`;
    return;
  }

  // ── Build author map ───────────────────────────────────────────────
  doc.querySelectorAll('authors > author').forEach(el => {
    const id = el.getAttribute('id');
    authors[id] = {
      id,
      name:     qs(el, 'name'),
      handle:   qs(el, 'handle'),
      initials: qs(el, 'initials') || id.slice(0, 2).toUpperCase(),
      color:    qs(el, 'color')    || '#888',
      textColor: qs(el, 'textcolor'),
      years:    qs(el, 'years'),
      bio:      qs(el, 'bio'),
      avatar:   qs(el, 'avatar'),
    };
  });

  // ── Handle map (handle string OR author id → author object, for @mention lookup) ──
  const handleMap = {};
  Object.entries(authors).forEach(([id, a]) => {
    if (a.handle) handleMap[a.handle] = a;
    handleMap[id] = a;  // also index by id so @emerson works alongside @rwemerson
  });

  // ── Render main posts ──────────────────────────────────────────────
  const posts = [...doc.querySelectorAll('thread > posts > post')];
  container.innerHTML = '';
  posts.forEach((postEl, i) => {
    container.appendChild(buildPost(postEl, /* isLast */ i === posts.length - 1));
  });

  // ── @mention hover (delegated) ─────────────────────────────────────
  container.addEventListener('mouseover', e => {
    if (e.target.classList.contains('mention')) {
      const author = handleMap[e.target.dataset.handle];
      if (author) showTooltip(e, author);
    }
  });
  container.addEventListener('mouseout', e => {
    if (e.target.classList.contains('mention')) tooltip.setAttribute('hidden', '');
  });

  // ── Builders ───────────────────────────────────────────────────────

  function buildPost(postEl, isLast) {
    const author      = getAuthor(postEl.getAttribute('author'));
    const timestamp   = postEl.getAttribute('timestamp') || '';
    const repliesNode = postEl.querySelector(':scope > replies');
    const threadItems = repliesNode ? [...repliesNode.children] : [];

    const wrapper = el('article', 'post-wrapper');
    if (!isLast) wrapper.classList.add('in-thread');

    const row = el('div', 'post-row');
    row.appendChild(buildAvatar(author, 40));
    row.appendChild(buildBody(postEl, author, timestamp, threadItems, null));
    wrapper.appendChild(row);

    if (threadItems.length) {
      const repliesArea = el('div', 'replies-area');
      threadItems.forEach(item => repliesArea.appendChild(buildThreadItem(item, 1)));
      wrapper.appendChild(repliesArea);

      const toggleBtn = row.querySelector('.reply-toggle-btn');
      if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
          const open = repliesArea.classList.toggle('open');
          toggleBtn.querySelector('.action-label').textContent =
            open ? 'Hide'
                 : `${threadItems.length} ${threadItems.length === 1 ? 'reply' : 'replies'}`;
        });
      }
    }

    return wrapper;
  }

  // Dispatches to the appropriate builder based on XML element name.
  function buildThreadItem(itemEl, depth) {
    if (itemEl.tagName === 'reply')  return buildReplyRow(itemEl, depth);
    if (itemEl.tagName === 'repost') return buildRepostRow(itemEl, depth);
  }

  // depth is 1-based; padding and avatar size scale with it.
  // Children (any depth) are always visible once the enclosing replies-area opens.
  function buildReplyRow(replyEl, depth) {
    const author      = getAuthor(replyEl.getAttribute('author'));
    const timestamp   = replyEl.getAttribute('timestamp') || '';
    const repliesNode = replyEl.querySelector(':scope > replies');
    const childItems  = repliesNode ? [...repliesNode.children] : [];

    const wrapper = el('div', 'reply-wrapper');
    const row = el('div', 'reply-row');
    row.style.paddingLeft = replyPad(depth) + 'px';

    row.appendChild(buildAvatar(author, depth === 1 ? 32 : 28));
    row.appendChild(buildBody(replyEl, author, timestamp, [], 'reply-body'));
    wrapper.appendChild(row);

    if (childItems.length) {
      const childArea = el('div', 'child-replies-area');
      childItems.forEach(child => childArea.appendChild(buildThreadItem(child, depth + 1)));
      wrapper.appendChild(childArea);
    }

    return wrapper;
  }

  function buildRepostRow(repostEl, depth) {
    const author      = getAuthor(repostEl.getAttribute('author'));
    const timestamp   = repostEl.getAttribute('timestamp') || '';
    const contentHtml = getContentHtml(repostEl);
    const likeEls     = getLikeEls(repostEl);
    const repliesNode = repostEl.querySelector(':scope > replies');
    const childItems  = repliesNode ? [...repliesNode.children] : [];

    const wrapper = el('div', 'repost-wrapper');
    const row = el('div', 'repost-row');
    row.style.paddingLeft = replyPad(depth) + 'px';

    row.appendChild(buildAvatar(author, depth === 1 ? 32 : 28));

    const body = el('div', 'repost-body');
    const hdr  = el('div', 'repost-header');
    const nameEl = el('span', 'post-name repost-name', author.name);
    addProfileHover(nameEl, author);
    hdr.append(el('span', 'repost-icon', '↻'), ' ', nameEl,
               el('span', 'repost-verb', ` reposted · ${timestamp}`));
    body.appendChild(hdr);

    if (contentHtml) {
      const cd = el('div', 'post-content repost-comment');
      cd.innerHTML = contentHtml;
      body.appendChild(cd);
    }

    if (likeEls.length) {
      const likerNames = likeEls.map(l => getAuthor(l.getAttribute('author')).name);
      const actions = el('div', 'post-actions');
      const btn = el('button', 'action-btn like-btn');
      btn.innerHTML = `<span class="action-icon">♥</span>
                       <span class="action-label">${likeEls.length}</span>
                       <span class="like-tooltip">Liked by: ${escHtml(likerNames.join(', '))}</span>`;
      actions.appendChild(btn);
      body.appendChild(actions);
    }

    row.appendChild(body);
    wrapper.appendChild(row);

    if (childItems.length) {
      const childArea = el('div', 'child-replies-area');
      childItems.forEach(child => childArea.appendChild(buildThreadItem(child, depth + 1)));
      wrapper.appendChild(childArea);
    }

    return wrapper;
  }

  // Left padding for a reply/repost at the given 1-based depth.
  // depth 1 → 52px, depth 2 → 76px, each level adds 24px.
  function replyPad(depth) { return 28 + depth * 24; }

  // Serialize a <content> child's nodes to HTML, preserving <em> and <strong>.
  function getContentHtml(xmlEl) {
    const child = xmlEl.querySelector(':scope > content');
    if (!child) return '';
    return [...child.childNodes].map(n => {
      if (n.nodeType === Node.TEXT_NODE) return mentionHtml(escHtml(n.textContent));
      if (n.nodeName === 'em')           return `<em>${mentionHtml(escHtml(n.textContent))}</em>`;
      if (n.nodeName === 'strong')       return `<strong>${mentionHtml(escHtml(n.textContent))}</strong>`;
      if (n.nodeName === 'br')           return '<br>';
      return mentionHtml(escHtml(n.textContent));
    }).join('');
  }

  // Wrap @handle tokens in styled spans for known cast members.
  function mentionHtml(s) {
    return s.replace(/@([\w-]+)/g, (match, handle) => {
      if (!handleMap[handle]) return match;
      return `<span class="mention" data-handle="${handle}">${match}</span>`;
    });
  }

  // Builds a quote-tweet box for a <quote> element.
  // Attributes: author="id" (registered) or name="Display Name" (non-cast),
  //             timestamp="...", source="..."
  function buildQuoteBox(quoteEl) {
    const box = el('div', 'quote-box');

    const authorId  = quoteEl.getAttribute('author');
    const timestamp = quoteEl.getAttribute('timestamp') || '';
    const source    = quoteEl.getAttribute('source')    || '';
    const authorObj = authorId ? getAuthor(authorId) : null;
    const name      = authorObj ? authorObj.name : (quoteEl.getAttribute('name') || '');

    const attr = el('div', 'quote-attribution');

    if (authorObj) attr.appendChild(buildAvatar(authorObj, 20));

    const nameSpan = el('span', 'quote-name', name);
    if (authorObj) addProfileHover(nameSpan, authorObj);
    attr.appendChild(nameSpan);

    if (authorObj) attr.appendChild(el('span', 'quote-handle', `@${authorObj.handle}`));
    if (timestamp)  attr.appendChild(el('span', 'quote-ts', timestamp));
    if (source)     attr.appendChild(el('span', 'quote-source', source));

    box.appendChild(attr);

    const contentDiv = el('div', 'quote-content');
    contentDiv.innerHTML = getContentHtml(quoteEl);
    box.appendChild(contentDiv);

    return box;
  }

  // Builds a Twitter-style link preview card for a <link> element.
  // Attributes: url, title, description (optional), thumb (optional image URL).
  function buildLinkCard(linkEl) {
    const url   = linkEl.getAttribute('url')         || '#';
    const title = linkEl.getAttribute('title')       || '';
    const desc  = linkEl.getAttribute('description') || '';
    const thumb = linkEl.getAttribute('thumb')       || '';
    const type  = linkEl.getAttribute('type')        || '';

    const a = document.createElement('a');
    a.className = 'link-card';
    a.href      = url;
    a.target    = '_blank';
    a.rel       = 'noopener noreferrer';

    if (thumb) {
      const img = document.createElement('img');
      img.className = 'link-card-thumb';
      img.src = thumb;
      img.alt = title;
      img.onerror = () => img.remove();
      a.appendChild(img);
    }

    const body = el('div', 'link-card-body');

    if (type === 'verse') {
      body.appendChild(el('div', 'link-card-domain', title));
      if (desc) body.appendChild(el('div', 'link-card-verse', desc));
    } else {
      try {
        const domain = new URL(url).hostname.replace(/^www\./, '');
        body.appendChild(el('div', 'link-card-domain', domain));
      } catch (_) {}
      body.appendChild(el('div', 'link-card-title', title));
      if (desc) body.appendChild(el('div', 'link-card-desc', desc));
    }

    a.appendChild(body);
    return a;
  }

  // Builds the right-side content column (header + content + actions).
  // bodyClass overrides the default 'post-body' class for reply variants.
  // threadItems is the array of <reply>/<repost> children (used only for count).
  function buildBody(xmlEl, author, timestamp, threadItems, bodyClass) {
    const body = el('div', bodyClass || 'post-body');

    // Header: Name @handle · timestamp
    const hdr = el('div', 'post-header');
    const nameEl = el('span', 'post-name', author.name);
    addProfileHover(nameEl, author);
    hdr.append(nameEl, ' ', el('span', 'post-handle', `@${author.handle}`),
               el('span', 'post-ts', timestamp));
    body.appendChild(hdr);

    // Content (preserves <em> and <strong>)
    const contentDiv = el('div', 'post-content');
    contentDiv.innerHTML = getContentHtml(xmlEl);
    body.appendChild(contentDiv);

    // Quote box (if present)
    const quoteEl = xmlEl.querySelector(':scope > quote');
    if (quoteEl) body.appendChild(buildQuoteBox(quoteEl));

    // Link card (if present)
    const linkEl = xmlEl.querySelector(':scope > link');
    if (linkEl) body.appendChild(buildLinkCard(linkEl));

    // Actions
    const likeEls = getLikeEls(xmlEl);
    const actions = el('div', 'post-actions');

    if (threadItems.length) {
      const btn = el('button', 'action-btn reply-toggle-btn');
      btn.innerHTML = `<span class="action-icon">💬</span>
                       <span class="action-label">${threadItems.length} ${threadItems.length === 1 ? 'reply' : 'replies'}</span>`;
      actions.appendChild(btn);
    }

    if (likeEls.length) {
      const likerNames = likeEls.map(l => getAuthor(l.getAttribute('author')).name);
      const btn = el('button', 'action-btn like-btn');
      btn.innerHTML = `<span class="action-icon">♥</span>
                       <span class="action-label">${likeEls.length}</span>
                       <span class="like-tooltip">Liked by: ${escHtml(likerNames.join(', '))}</span>`;
      actions.appendChild(btn);
    }

    body.appendChild(actions);
    return body;
  }

  function buildAvatar(author, size) {
    const div = el('div', 'avatar');
    div.style.cssText =
      `width:${size}px;height:${size}px;background-color:${author.color};` +
      `font-size:${Math.round(size * 0.375)}px;flex-shrink:0` +
      (author.textColor ? `;color:${author.textColor}` : '');

    if (author.avatar) {
      const img = document.createElement('img');
      img.src = author.avatar;
      img.alt = author.name;
      img.onerror = () => { img.remove(); div.textContent = author.initials; };
      div.appendChild(img);
    } else {
      div.textContent = author.initials;
    }

    addProfileHover(div, author);
    return div;
  }

  // ── Profile tooltip ────────────────────────────────────────────────

  function addProfileHover(target, author) {
    target.addEventListener('mouseenter', (e) => showTooltip(e, author));
    target.addEventListener('mouseleave', () => tooltip.setAttribute('hidden', ''));
  }

  function showTooltip(e, author) {
    const ttAvatar = tooltip.querySelector('.tt-avatar');
    ttAvatar.style.backgroundColor = author.color;
    ttAvatar.textContent = '';

    if (author.avatar) {
      const img = document.createElement('img');
      img.src = author.avatar;
      img.alt = author.name;
      img.onerror = () => { img.remove(); ttAvatar.textContent = author.initials; };
      ttAvatar.appendChild(img);
    } else {
      ttAvatar.textContent = author.initials;
    }

    tooltip.querySelector('.tt-name').textContent   = author.name;
    tooltip.querySelector('.tt-handle').textContent = `@${author.handle}`;
    tooltip.querySelector('.tt-bio').textContent    = author.bio;
    tooltip.querySelector('.tt-years').textContent  = author.years;

    tooltip.removeAttribute('hidden');
    positionTooltip(e.target);
  }

  function positionTooltip(target) {
    const r   = target.getBoundingClientRect();
    const tw  = 300;
    const th  = 180; // estimated tooltip height
    let left  = r.left;
    let top   = r.bottom + 8;

    if (left + tw > window.innerWidth - 8)  left = window.innerWidth - tw - 8;
    if (left < 8)                            left = 8;
    if (top + th > window.innerHeight - 8)  top  = r.top - th - 8;

    tooltip.style.left = left + 'px';
    tooltip.style.top  = top  + 'px';
  }

  // ── Utilities ──────────────────────────────────────────────────────

  // Get all <like> elements: supports both <likes><like/></likes> and bare <like/>
  function getLikeEls(el) {
    return [
      ...el.querySelectorAll(':scope > likes > like'),
      ...el.querySelectorAll(':scope > like'),
    ];
  }

  // Get text of a direct child element by tag name
  function qs(parent, tag) {
    const child = parent.querySelector(`:scope > ${tag}`);
    return child ? child.textContent.trim() : '';
  }

  function getAuthor(id) {
    return authors[id] || {
      id, name: id, handle: id,
      initials: (id || '?').slice(0, 2).toUpperCase(),
      color: '#888', years: '', bio: '', avatar: '',
    };
  }

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls)  node.className   = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
