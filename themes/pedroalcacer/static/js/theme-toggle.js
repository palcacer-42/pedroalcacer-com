/* Theme toggle helper
   - Initializes `data-theme` on <html> using localStorage or system preference
   - Exposes `window.toggleTheme()` for a UI toggle (doesn't add UI itself)
*/
(function () {
  try {
    var stored = localStorage.getItem('theme');
    var theme = stored || 'light';
    document.documentElement.setAttribute('data-theme', theme);
  } catch (e) {
    /* swallow errors for older browsers */
  }

  window.toggleTheme = function () {
    try {
      var cur = document.documentElement.getAttribute('data-theme') || 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    } catch (e) {}
  };
})();
