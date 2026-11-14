/**
 * Design tokens for canvas and chart code.
 *
 * CSS custom properties are the single source of truth for colour (app/static/css/style.css,
 * :root). Anything drawn from JavaScript reads them here, so a theme change is a CSS change
 * and never a hunt for hex codes in scripts.
 *
 * Call tokens() when you create the thing that draws (after the stylesheet has loaded), not
 * at module load.
 */
export function tokens() {
  const cs = getComputedStyle(document.documentElement);
  const v = (name) => cs.getPropertyValue(name).trim();
  return {
    bg: v("--bg"), ink: v("--ink"), muted: v("--muted"),
    line: v("--line"), lineFaint: v("--line-faint"), surface: v("--surface"),
    signal: v("--signal"),
    // status colours, keyed the way the API names bands
    GREEN: v("--nominal"), YELLOW: v("--checkin"), RED: v("--review"),
    font: v("--font"),
  };
}
