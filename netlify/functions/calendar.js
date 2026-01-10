const axios = require('axios');
const ical = require('ical');

// Netlify Function to fetch public Google Calendar ICS and return parsed upcoming events as JSON.
// Set environment variable CALENDAR_ICS_URL or CALENDAR_ID to configure.

exports.handler = async function(event, context) {
  try {
    const CALENDAR_ICS_URL = process.env.CALENDAR_ICS_URL || (process.env.CALENDAR_ID ? `https://calendar.google.com/calendar/ical/${encodeURIComponent(process.env.CALENDAR_ID)}/public/basic.ics` : null);
    if(!CALENDAR_ICS_URL){
      return { statusCode: 400, body: JSON.stringify({ error: 'CALENDAR_ICS_URL or CALENDAR_ID not configured' }) };
    }
    const resp = await axios.get(CALENDAR_ICS_URL, { responseType: 'text', timeout: 15000 });
    const data = resp.data;
    const parsed = ical.parseICS(data);
    const now = new Date();
    const events = [];
    for(const k of Object.keys(parsed)){
      const ev = parsed[k];
      if(ev.type === 'VEVENT'){
        const start = ev.start instanceof Date ? ev.start : null;
        if(!start) continue;
        if(start < now) continue;
        events.push({
          title: ev.summary || '',
          start: start.toISOString(),
          end: ev.end ? ev.end.toISOString() : null,
          location: ev.location || '',
          description: ev.description || '',
          url: ev.url || ''
        });
      }
    }
    events.sort((a,b)=> new Date(a.start) - new Date(b.start));
    const maxResults = process.env.MAX_RESULTS ? parseInt(process.env.MAX_RESULTS,10) : 8;
    const out = events.slice(0, maxResults);
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300'
      },
      body: JSON.stringify(out)
    };
  } catch(err){
    console.error('calendar function error', err && err.message);
    return { statusCode: 500, body: JSON.stringify({ error: 'failed to fetch or parse calendar' }) };
  }
};
