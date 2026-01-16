(function () {
  const el = document.getElementById('google-calendar-widget');
  if (!el) return;
  const calendarId = el.dataset.calendarId;
  const apiKey = el.dataset.apiKey;
  const endpoint = el.dataset.endpoint;

  function showMessage(msg, cls = 'gc-loading') {
    el.innerHTML = `<div class="${cls}">${msg}</div>`;
  }

  // If a serverless endpoint is provided, use it (no API keys needed client-side)
  if (endpoint) {
    fetch(endpoint).then(resp => {
      if (!resp.ok) throw new Error('Network response not ok');
      return resp.json();
    }).then(data => {
      if (!data || data.length === 0) {
        showMessage('No upcoming concerts.', 'gc-empty');
        return;
      }
      const ul = document.createElement('ul');
      ul.className = 'gc-list';
      data.forEach(ev => {
        const d = ev.start ? new Date(ev.start) : null;
        const li = document.createElement('li');
        li.className = 'gc-item';
        const title = ev.title || 'Event';
        const locHtml = ev.location ? `<span class="gc-location">${escapeHtml(ev.location)}</span>` : '';
        const dateLine1 = d ? new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric' }).format(d) : '';
        const dateLine2 = d ? new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(d) : '';
        // If event description contains a URL, prefer it as link
        const url = ev.url || (ev.description && findFirstUrl(ev.description));
        const titleContent = escapeHtml(title);
        const titleLinkHtml = url ? `<a class="gc-title-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${titleContent}</a>` : `<span class="gc-title-text">${titleContent}</span>`;
        const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g, '<br>') : '';
        const detailsHtml = `
          <details>
            <summary>
              <div class="gc-summary-left">${titleLinkHtml}<span class="gc-expander" aria-hidden="true">▸</span>${locHtml}</div>
              <div class="gc-summary-date"><span class="gc-date-line1">${escapeHtml(dateLine1)}</span><span class="gc-date-line2">${escapeHtml(dateLine2)}</span></div>
            </summary>
            <div class="gc-details">${desc}${url && !ev.url ? `<div class="gc-more"><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">More info</a></div>` : ''}</div>
          </details>`;
        li.innerHTML = detailsHtml;
        ul.appendChild(li);
        // prevent title link clicks from toggling the details
        const link = li.querySelector('.gc-title-link');
        if (link) {
          // First click: expand the <details>. Second click (when open): follow the link.
          link.addEventListener('click', function (e) {
            const details = this.closest('details');
            if (details && !details.open) {
              e.preventDefault();
              e.stopPropagation();
              details.open = true;
              // move focus back to the summary so keyboard users remain oriented
              const summary = details.querySelector('summary');
              if (summary) summary.focus();
            }
            // if already open, allow the default (link opens in new tab)
          });
          link.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
              const details = this.closest('details');
              if (details && !details.open) {
                e.preventDefault();
                e.stopPropagation();
                details.open = true;
                const summary = details.querySelector('summary');
                if (summary) summary.focus();
              }
              // otherwise let the keypress follow the link (target _blank)
            }
          });
        }
        // (no interception) title link opens in new tab
      });
      el.innerHTML = '';
      const container = document.createElement('div');
      container.className = 'gc-list-container';
      container.tabIndex = 0;
      container.setAttribute('aria-label', 'Upcoming concerts');
      container.appendChild(ul);
      el.appendChild(container);
    }).catch(err => {
      console.error('Calendar endpoint error', err);
      showMessage('Could not load calendar.', 'gc-error');
    });
    return;
  }

  // Fallback to Google API if apiKey is present
  if (!calendarId) {
    showMessage('Calendar not configured. Add the calendar ID to site params.', 'gc-error');
    return;
  }
  if (!apiKey) {
    // No API key available — render the public Google Calendar embed iframe as a fallback.
    // This requires the calendar to be public (no API usage).
    const wrap = document.createElement('div');
    wrap.className = 'calendar-embed';
    const embedUrl = `https://calendar.google.com/calendar/embed?src=${encodeURIComponent(calendarId)}&ctz=Europe%2FBerlin`;
    wrap.innerHTML = `<iframe src="${embedUrl}" style="border:0" width="100%" height="300" frameborder="0" scrolling="no"></iframe>`;
    el.innerHTML = '';
    el.appendChild(wrap);
    return;
  }

  // Fetch all events (up to 2000) by removing timeMin and increasing maxResults
  const maxResults = 2000;
  const url = `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events?key=${encodeURIComponent(apiKey)}&singleEvents=true&orderBy=startTime&maxResults=${maxResults}`;

  fetch(url).then(resp => {
    if (!resp.ok) {
      return resp.text().then(t => { throw new Error(`HTTP ${resp.status}: ${t}`); });
    }
    return resp.json();
  }).then(data => {
    if (!data.items || data.items.length === 0) {
      showMessage('No concerts found.', 'gc-empty');
      return;
    }

    const now = new Date();
    // Sort ALL events chronologically: Oldest -> Newest
    const events = data.items.filter(ev => ev.status !== 'cancelled' && (ev.start.dateTime || ev.start.date));
    events.sort((a, b) => {
      const da = new Date(a.start.dateTime || a.start.date);
      const db = new Date(b.start.dateTime || b.start.date);
      return da - db;
    });

    const ul = document.createElement('ul');
    ul.className = 'gc-list';

    let dividerInserted = false;

    events.forEach((ev, index) => {
      const start = ev.start && (ev.start.dateTime || ev.start.date);
      const d = new Date(start);

      // Check if we need to insert the divider
      // We insert it before the first event that is in the future
      // OR if we are at the end and haven't inserted it (implied all past?) - logic below handles "first future event"
      if (!dividerInserted && d >= now) {
        const liDivider = document.createElement('li');
        liDivider.className = 'gc-datum-line';
        liDivider.id = 'gc-today-marker';
        liDivider.innerHTML = `<span>NEXT</span><div class="gc-line"></div>`;
        ul.appendChild(liDivider);
        dividerInserted = true;
      }

      const li = document.createElement('li');
      li.className = 'gc-item';
      // Optional: add class for past/future styling if needed
      if (d < now) {
        li.classList.add('gc-item-past');
      }

      const title = ev.summary || 'Event';
      const locHtml = ev.location ? `<span class="gc-location">${escapeHtml(ev.location)}</span>` : '';
      const dateLine1 = d ? new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }).format(d) : '';
      const dateLine2 = d ? new Intl.DateTimeFormat(undefined, { hour: '2-digit', minute: '2-digit' }).format(d) : '';

      const url = ev.htmlLink || ev.url || '';
      const titleContent = escapeHtml(title);
      const titleLinkHtml = url ? `<a class="gc-title-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${titleContent}</a>` : `<span class="gc-title-text">${titleContent}</span>`;
      const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g, '<br>') : '';

      const detailsHtml = `
        <details>
          <summary>
            <div class="gc-summary-left">${titleLinkHtml}<span class="gc-expander" aria-hidden="true">▸</span>${locHtml}</div>
            <div class="gc-summary-date"><span class="gc-date-line1">${escapeHtml(dateLine1)}</span><span class="gc-date-line2">${escapeHtml(dateLine2)}</span></div>
          </summary>
          <div class="gc-details">${desc}${url && !ev.url ? `<div class="gc-more"><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">More info</a></div>` : ''}</div>
        </details>`;
      li.innerHTML = detailsHtml;
      ul.appendChild(li);

      // Re-attach listeners (same as before)
      const link = li.querySelector('.gc-title-link');
      if (link) {
        link.addEventListener('click', function (e) {
          const details = this.closest('details');
          if (details && !details.open) {
            e.preventDefault();
            e.stopPropagation();
            details.open = true;
            const summary = details.querySelector('summary');
            if (summary) summary.focus();
          }
        });
        link.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') {
            const details = this.closest('details');
            if (details && !details.open) {
              e.preventDefault();
              e.stopPropagation();
              details.open = true;
              const summary = details.querySelector('summary');
              if (summary) summary.focus();
            }
          }
        });
      }
    });

    // If all events were in the past and we never inserted the divider, insert it at the end?
    // Or if all events are in the future, it would be at the start.
    // The loop logic 'd >= now' handles "all future" (inserts at index 0).
    // If "all past", dividerInserted remains false. Let's append it at the end to show "Now".
    if (!dividerInserted) {
      const liDivider = document.createElement('li');
      liDivider.className = 'gc-datum-line';
      liDivider.id = 'gc-today-marker';
      liDivider.innerHTML = `<span>NEXT</span><div class="gc-line"></div>`;
      ul.appendChild(liDivider);
    }

    el.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'gc-list-container';
    container.tabIndex = 0;
    container.setAttribute('aria-label', 'Concert Calendar');
    container.appendChild(ul);
    el.appendChild(container);

    // Auto-scroll to the divider
    // We need a slight delay to ensure rendering is done? Usually synchronous in simple DOM, 
    // but good practice to let the browser paint or layout first if needed.
    // However, scrolling immediately usually works.
    setTimeout(() => {
      const marker = document.getElementById('gc-today-marker');
      if (marker && container) {
        // Scroll logic: center the marker
        // container.scrollTop = marker.offsetTop - (container.clientHeight / 2) + (marker.clientHeight / 2);
        marker.scrollIntoView({ behavior: 'auto', block: 'center' });
      }
    }, 0);

  }).catch(err => {
    console.error('Google Calendar fetch error', err);
    showMessage('Could not load calendar — check API key and calendar visibility.', 'gc-error');
  });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": "&#39;" }[c];
    });
  }

  function findFirstUrl(text) {
    if (!text) return null;
    // Try to find an http(s) URL or a www. URL. Trim trailing punctuation.
    const re = /(https?:\/\/[^\s<>"')]+)|(www\.[^\s<>"')]+)/i;
    const m = text.match(re);
    if (!m) return null;
    let url = m[0];
    // If it starts with www., add protocol
    if (/^www\./i.test(url)) url = 'https://' + url;
    // Trim trailing punctuation characters
    url = url.replace(/[\.\,;:\)\]\!\?]+$/, '');
    return url;
  }

  // Modal helpers
  let _modal = null;
  function showModal(ev) {
    closeModal();
    const title = escapeHtml(ev.title || 'Event');
    const date = ev.start ? new Date(ev.start) : null;
    const dateStr = date ? new Intl.DateTimeFormat(undefined, { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(date) : '';
    const location = ev.location ? escapeHtml(ev.location) : '';
    const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g, '<br>') : '';
    const url = ev.url || (ev.description && findFirstUrl(ev.description)) || '';

    const overlay = document.createElement('div');
    overlay.className = 'gc-modal-overlay';

    const dialog = document.createElement('div');
    dialog.className = 'gc-modal-dialog';

    const closeBtn = document.createElement('button');
    closeBtn.className = 'gc-modal-close';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.innerHTML = '✕';
    closeBtn.addEventListener('click', closeModal);

    const h = document.createElement('h4');
    h.className = 'gc-modal-title';
    h.innerHTML = title;

    const meta = document.createElement('div');
    meta.className = 'gc-modal-meta';
    meta.innerHTML = `<span class="gc-date">${escapeHtml(dateStr)}</span>${location ? '<span class="gc-location"> — ' + location + '</span>' : ''}`;

    const content = document.createElement('div');
    content.className = 'gc-modal-content';
    content.innerHTML = desc || '<em>No additional information.</em>';

    const actions = document.createElement('div');
    actions.className = 'gc-modal-actions';
    if (url) {
      const a = document.createElement('a');
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'gc-modal-link';
      a.textContent = 'Open link';
      actions.appendChild(a);
    }

    dialog.appendChild(closeBtn);
    dialog.appendChild(h);
    dialog.appendChild(meta);
    dialog.appendChild(content);
    dialog.appendChild(actions);

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);
    _modal = overlay;

    // accessibility
    overlay.tabIndex = -1;
    overlay.focus();
    function onKey(e) { if (e.key === 'Escape') closeModal(); }
    overlay._keyHandler = onKey;
    document.addEventListener('keydown', onKey);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  }

  function closeModal() {
    if (!_modal) return;
    document.removeEventListener('keydown', _modal._keyHandler);
    _modal.remove();
    _modal = null;
  }
})();
