/**
 * Google Apps Script: export active sheet to JSON and commit to GitHub
 *
 * Requirements (Script Properties):
 *  - GITHUB_TOKEN: a Personal Access Token with 'repo' (or 'public_repo') scope
 *  - REPO_OWNER: GitHub owner/org (e.g. palcacer)
 *  - REPO_NAME: repository name (e.g. pedroalcacer-com)
 *  - FILE_PATH: path in the repo to write (e.g. data/concerts.json)
 *  - COMMITTER_NAME (optional)
 *  - COMMITTER_EMAIL (optional)
 *
 * Usage: set the above properties in Project Settings (Script Properties) and run `pushSheetToGit()`
 */

function pushSheetToGit() {
  const props = PropertiesService.getScriptProperties();
  const token = props.getProperty('GITHUB_TOKEN');
  const owner = props.getProperty('REPO_OWNER');
  const repo = props.getProperty('REPO_NAME');
  const path = props.getProperty('FILE_PATH') || 'data/concerts.json';
  const committerName = props.getProperty('COMMITTER_NAME') || 'Sheet Sync';
  const committerEmail = props.getProperty('COMMITTER_EMAIL') || 'sheet-sync@example.com';

  if (!token || !owner || !repo) {
    throw new Error('Missing script properties: GITHUB_TOKEN, REPO_OWNER, REPO_NAME');
  }

  // Read sheet
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getActiveSheet();
  const values = sheet.getDataRange().getValues();
  if (values.length < 2) {
    throw new Error('Sheet must have header row + data rows');
  }

  const headers = values[0].map(h => String(h).trim());
  const records = [];
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    // skip empty rows
    if (row.every(c => c === '' || c === null)) continue;
    const obj = {};
    for (let j = 0; j < headers.length; j++) {
      obj[headers[j]] = row[j] === undefined ? '' : row[j];
    }
    records.push(obj);
  }

  const content = JSON.stringify(records, null, 2);
  const b64 = Utilities.base64Encode(content);

  const apiBase = 'https://api.github.com';
  const fileUrl = `${apiBase}/repos/${owner}/${repo}/contents/${encodeURIComponent(path)}`;

  // Get existing file to obtain SHA (if exists)
  const getOpts = {
    method: 'get',
    headers: { Authorization: 'token ' + token, Accept: 'application/vnd.github.v3+json' },
    muteHttpExceptions: true
  };
  const getResp = UrlFetchApp.fetch(fileUrl, getOpts);
  let sha = null;
  if (getResp.getResponseCode() === 200) {
    const body = JSON.parse(getResp.getContentText());
    sha = body.sha;
  }

  const payload = {
    message: `Update concerts.json from sheet (${new Date().toISOString().slice(0,10)})`,
    content: b64,
    committer: { name: committerName, email: committerEmail }
  };
  if (sha) payload.sha = sha;

  const putOpts = {
    method: 'put',
    headers: { Authorization: 'token ' + token, Accept: 'application/vnd.github.v3+json' },
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const putResp = UrlFetchApp.fetch(fileUrl, putOpts);
  const status = putResp.getResponseCode();
  if (status >= 200 && status < 300) {
    Logger.log('File committed successfully');
    return JSON.parse(putResp.getContentText());
  } else {
    throw new Error('GitHub API error: ' + status + ' ' + putResp.getContentText());
  }
}
