-- Crew Readiness — SQLite schema (prototype).
-- Mirrors docs/DATA_CONTRACT.md. Note what is NOT here: there is no column
-- that could hold typed text, key identities, or raw keystroke timelines.

DROP TABLE IF EXISTS attention_results;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS profiles;

-- kind = 'demo'      -> fictional crew member with synthetic data (for the pitch)
-- kind = 'team_test' -> pseudonymous teammate doing real validation sessions
CREATE TABLE profiles (
  id            TEXT PRIMARY KEY,           -- slug, e.g. 'plt-okafor'
  display_name  TEXT NOT NULL,
  mission_role  TEXT NOT NULL,
  kind          TEXT NOT NULL DEFAULT 'demo' CHECK (kind IN ('demo', 'team_test')),
  created_at    TEXT NOT NULL
);

-- One row per completed task. Aggregate timing features only.
CREATE TABLE sessions (
  id                            INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_id                    TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  task_type                     TEXT NOT NULL,
  created_at                    TEXT NOT NULL,          -- ISO-8601 UTC, set by server
  source                        TEXT NOT NULL CHECK (source IN ('live', 'synthetic')),
  data_quality                  TEXT NOT NULL CHECK (data_quality IN ('ok', 'low')),
  quality_notes                 TEXT,
  keystroke_count               INTEGER NOT NULL,
  iki_median_ms                 REAL NOT NULL,
  iki_iqr_ms                    REAL NOT NULL,
  pause_count                   INTEGER NOT NULL,
  pause_total_ms                REAL NOT NULL,
  checklist_response_median_ms  REAL NOT NULL,
  task_duration_ms              REAL NOT NULL,
  correction_count              INTEGER NOT NULL,
  retry_count                   INTEGER NOT NULL,
  accepted_at                   TEXT                    -- set when a human accepts a flagged run as the new normal
);

CREATE INDEX idx_sessions_profile_task ON sessions (profile_id, task_type, id);

-- Optional reaction-time attention check (stretch feature, see TEAM_GUIDE task A-1).
CREATE TABLE attention_results (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  profile_id       TEXT NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  session_id       INTEGER REFERENCES sessions(id) ON DELETE SET NULL,
  created_at       TEXT NOT NULL,
  trials           INTEGER NOT NULL,
  median_rt_ms     REAL,                   -- NULL if every trial was missed
  premature_count  INTEGER NOT NULL,
  miss_count       INTEGER NOT NULL,
  lapse_count      INTEGER NOT NULL DEFAULT 0   -- responses over 355 ms plus misses (the PVT-B convention); added 2026-11-15
);
