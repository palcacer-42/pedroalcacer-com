(function(){
  const el = document.getElementById('google-calendar-widget');
  if(!el) return;
  const calendarId = el.dataset.calendarId;
  const apiKey = el.dataset.apiKey;
  const endpoint = el.dataset.endpoint;

  function showMessage(msg, cls='gc-loading'){
    el.innerHTML = `<div class="${cls}">${msg}</div>`;
  }

  // If a serverless endpoint is provided, use it (no API keys needed client-side)
  if(endpoint){
    fetch(endpoint).then(resp=>{
      if(!resp.ok) throw new Error('Network response not ok');
      return resp.json();
    }).then(data=>{
      if(!data || data.length===0){
        showMessage('No upcoming concerts.', 'gc-empty');
        return;
      }
      const ul = document.createElement('ul');
      ul.className = 'gc-list';
      data.forEach(ev=>{
        const d = ev.start ? new Date(ev.start) : null;
        const li = document.createElement('li');
        li.className = 'gc-item';
        const title = ev.title || 'Event';
        const locHtml = ev.location ? `<span class="gc-location"> — ${escapeHtml(ev.location)}</span>` : '';
        const dateStr = d ? new Intl.DateTimeFormat(undefined, {weekday:'short', month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'}).format(d) : '';
        // If event description contains a URL, prefer it as link
        const url = ev.url || (ev.description && findFirstUrl(ev.description));
        const titleContent = escapeHtml(title);
        const titleLinkHtml = url ? `<a class="gc-title-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${titleContent}</a>` : `<span class="gc-title-text">${titleContent}</span>`;
        const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g, '<br>') : '';
        const detailsHtml = `
          <details>
            <summary>
              ${titleLinkHtml}
              <span class="gc-expander" aria-hidden="true">▸</span>
              <span class="gc-date">${escapeHtml(dateStr)}</span>${locHtml}
            </summary>
            <div class="gc-details">${desc}${url && !ev.url ? `<div class="gc-more"><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">More info</a></div>` : ''}</div>
          </details>`;
        li.innerHTML = detailsHtml;
        ul.appendChild(li);
        // prevent title link clicks from toggling the details
        const link = li.querySelector('.gc-title-link');
        if(link){
          // First click: expand the <details>. Second click (when open): follow the link.
          link.addEventListener('click', function(e){
            const details = this.closest('details');
            if(details && !details.open){
              e.preventDefault();
              e.stopPropagation();
              details.open = true;
              // move focus back to the summary so keyboard users remain oriented
              const summary = details.querySelector('summary');
              if(summary) summary.focus();
            }
            // if already open, allow the default (link opens in new tab)
          });
          link.addEventListener('keydown', function(e){
            if(e.key === 'Enter' || e.key === ' '){
              const details = this.closest('details');
              if(details && !details.open){
                e.preventDefault();
                e.stopPropagation();
                details.open = true;
                const summary = details.querySelector('summary');
                if(summary) summary.focus();
              }
              // otherwise let the keypress follow the link (target _blank)
            }
          });
        }
        // (no interception) title link opens in new tab
      });
      el.innerHTML = '';
      el.appendChild(ul);
    }).catch(err=>{
      console.error('Calendar endpoint error', err);
      showMessage('Could not load calendar.', 'gc-error');
    });
    return;
  }

  // Fallback to Google API if apiKey is present
  if(!calendarId){
    showMessage('Calendar not configured. Add the calendar ID to site params.', 'gc-error');
    return;
  }
  if(!apiKey){
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

  const now = new Date().toISOString();
  const maxResults = 8;
  const url = `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calendarId)}/events?key=${encodeURIComponent(apiKey)}&timeMin=${encodeURIComponent(now)}&singleEvents=true&orderBy=startTime&maxResults=${maxResults}`;

  fetch(url).then(resp=>{
    if(!resp.ok){
      return resp.text().then(t=>{ throw new Error(`HTTP ${resp.status}: ${t}`); });
    }
    return resp.json();
  }).then(data=>{
    if(!data.items || data.items.length===0){
      showMessage('No upcoming concerts found.', 'gc-empty');
      return;
    }
    const ul = document.createElement('ul');
    ul.className = 'gc-list';
    data.items.forEach(ev=>{
      const start = ev.start && (ev.start.dateTime || ev.start.date);
      const d = start ? new Date(start) : null;
      const li = document.createElement('li');
      li.className = 'gc-item';
      const title = ev.summary || 'Event';
      const locHtml = ev.location ? `<span class="gc-location"> — ${escapeHtml(ev.location)}</span>` : '';
      const dateStr = d ? new Intl.DateTimeFormat(undefined, {weekday:'short', month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'}).format(d) : '';
      const url = ev.htmlLink || ev.htmlLink || ev.url || '';
      const titleContent = escapeHtml(title);
      const titleLinkHtml = url ? `<a class="gc-title-link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${titleContent}</a>` : `<span class="gc-title-text">${titleContent}</span>`;
      const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g, '<br>') : '';
      li.innerHTML = `
        <details>
          <summary>
            ${titleLinkHtml}
            <span class="gc-expander" aria-hidden="true">▸</span>
            <span class="gc-date">${escapeHtml(dateStr)}</span>${locHtml}
          </summary>
          <div class="gc-details">${desc}${url && !ev.url ? `<div class="gc-more"><a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">More info</a></div>` : ''}</div>
        </details>`;
      ul.appendChild(li);
      const link = li.querySelector('.gc-title-link');
      if(link){
        // First click: expand the <details>. Second click (when open): follow the link.
        link.addEventListener('click', function(e){
          const details = this.closest('details');
          if(details && !details.open){
            e.preventDefault();
            e.stopPropagation();
            details.open = true;
            const summary = details.querySelector('summary');
            if(summary) summary.focus();
          }
        });
        link.addEventListener('keydown', function(e){
          if(e.key === 'Enter' || e.key === ' '){
            const details = this.closest('details');
            if(details && !details.open){
              e.preventDefault();
              e.stopPropagation();
              details.open = true;
              const summary = details.querySelector('summary');
              if(summary) summary.focus();
            }
          }
        });
      }
      // (no interception) title link opens in new tab
    });
    el.innerHTML = '';
    el.appendChild(ul);
  }).catch(err=>{
    console.error('Google Calendar fetch error', err);
    showMessage('Could not load calendar — check API key and calendar visibility.', 'gc-error');
  });

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[c];
    });
  }

  function findFirstUrl(text){
    if(!text) return null;
    // Try to find an http(s) URL or a www. URL. Trim trailing punctuation.
    const re = /(https?:\/\/[^\s<>"')]+)|(www\.[^\s<>"')]+)/i;
    const m = text.match(re);
    if(!m) return null;
    let url = m[0];
    // If it starts with www., add protocol
    if(/^www\./i.test(url)) url = 'https://' + url;
    // Trim trailing punctuation characters
    url = url.replace(/[\.\,;:\)\]\!\?]+$/,'');
    return url;
  }

  // Modal helpers
  let _modal = null;
  function showModal(ev){
    closeModal();
    const title = escapeHtml(ev.title || 'Event');
    const date = ev.start ? new Date(ev.start) : null;
    const dateStr = date ? new Intl.DateTimeFormat(undefined, {weekday:'short', month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'}).format(date) : '';
    const location = ev.location ? escapeHtml(ev.location) : '';
    const desc = ev.description ? escapeHtml(ev.description).replace(/\n/g,'<br>') : '';
    const url = ev.url || (ev.description && findFirstUrl(ev.description)) || '';

    const overlay = document.createElement('div');
    overlay.className = 'gc-modal-overlay';

    const dialog = document.createElement('div');
    dialog.className = 'gc-modal-dialog';

    const closeBtn = document.createElement('button');
    closeBtn.className = 'gc-modal-close';
    closeBtn.setAttribute('aria-label','Close');
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
    if(url){
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
    function onKey(e){ if(e.key === 'Escape') closeModal(); }
    overlay._keyHandler = onKey;
    document.addEventListener('keydown', onKey);
    overlay.addEventListener('click', function(e){ if(e.target === overlay) closeModal(); });
  }

  function closeModal(){
    if(!_modal) return;
    document.removeEventListener('keydown', _modal._keyHandler);
    _modal.remove();
    _modal = null;
  }
})();
