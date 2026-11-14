/**
 * Privacy-preserving timing capture.
 *
 * WHAT WE KEEP IN MEMORY: timestamps (performance.now()) and counters.
 * WHAT WE NEVER KEEP:     which key was pressed, or any typed text.
 * WHAT LEAVES THE BROWSER: only the aggregate numbers from summarize().
 *
 * `event.key` is looked at for one instant to classify the press as
 * "character", "correction" or "ignore" — it is never stored.
 *
 * The output shape MUST match app/features.py and docs/DATA_CONTRACT.md.
 * Owner: Member 3 (Frontend). Changes need Member 2 + team lead review.
 */

export const PAUSE_MS = 2000; // a gap this long inside an item counts as a pause

export function median(values) {
  if (values.length === 0) return 0;
  const s = [...values].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

/** Linear-interpolated quantile, same method as numpy's default. */
export function quantile(values, q) {
  if (values.length === 0) return 0;
  const s = [...values].sort((a, b) => a - b);
  const pos = (s.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  return s[lo] + (s[hi] - s[lo]) * (pos - lo);
}

function classify(event) {
  if (event.repeat) return "ignore"; // key held down — not a real press
  if (event.key === "Backspace" || event.key === "Delete") return "correction";
  if (event.key.length === 1 && !event.ctrlKey && !event.metaKey) return "char";
  return "ignore"; // Shift, Enter, arrows, Tab...
}

export function createCapture() {
  const items = [];
  let current = null;
  let taskStartedAt = null;
  let retries = 0;

  return {
    startTask(now = performance.now()) {
      taskStartedAt = now;
    },

    startItem(now = performance.now()) {
      current = { shownAt: now, firstKeyAt: null, lastKeyAt: null,
                  ikis: [], pauses: [], keys: 0, corrections: 0 };
    },

    /**
     * Call from a keydown listener. Stores a timestamp, never the key.
     * Returns true if the press was counted, so the UI can draw a blip. It never reports
     * which key it was.
     */
    onKeyDown(event, now = performance.now()) {
      if (!current) return false;
      const kind = classify(event);
      if (kind === "ignore") return false;
      if (kind === "correction") current.corrections += 1;
      current.keys += 1;
      if (current.firstKeyAt === null) {
        current.firstKeyAt = now;
      } else {
        const gap = now - current.lastKeyAt;
        if (gap >= PAUSE_MS) current.pauses.push(gap);
        else current.ikis.push(gap);
      }
      current.lastKeyAt = now;
      return true;
    },

    /** The typed confirmation did not match — the person has to re-enter it. */
    recordRetry() {
      retries += 1;
    },

    endItem() {
      if (current) items.push(current);
      current = null;
    },

    /** Aggregate features — the ONLY thing sent to the server. */
    summarize(now = performance.now()) {
      const ikis = items.flatMap((it) => it.ikis);
      const pauses = items.flatMap((it) => it.pauses);
      const responses = items
        .filter((it) => it.firstKeyAt !== null)
        .map((it) => it.firstKeyAt - it.shownAt);
      const r1 = (x) => Math.round(x * 10) / 10;

      return {
        keystroke_count: items.reduce((n, it) => n + it.keys, 0),
        iki_median_ms: r1(median(ikis)),
        iki_iqr_ms: r1(quantile(ikis, 0.75) - quantile(ikis, 0.25)),
        pause_count: pauses.length,
        pause_total_ms: r1(pauses.reduce((a, b) => a + b, 0)),
        checklist_response_median_ms: r1(median(responses)),
        task_duration_ms: r1(now - taskStartedAt),
        correction_count: items.reduce((n, it) => n + it.corrections, 0),
        retry_count: retries,
      };
    },
  };
}
