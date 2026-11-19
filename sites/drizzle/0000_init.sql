CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY, csrf TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS places (
  id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  label TEXT NOT NULL, street TEXT NOT NULL, number TEXT NOT NULL, neighborhood TEXT NOT NULL,
  city TEXT NOT NULL, state TEXT NOT NULL, postal_code TEXT NOT NULL, zone TEXT NOT NULL,
  chuva INTEGER NOT NULL, calor INTEGER NOT NULL, consent INTEGER NOT NULL, created_at TEXT NOT NULL,
  UNIQUE(session_id,street,number,zone)
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS notices (
  id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  code TEXT NOT NULL, version INTEGER NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL,
  UNIQUE(session_id,code,version)
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
  notice_id TEXT NOT NULL REFERENCES notices(id) ON DELETE CASCADE,
  created_at TEXT NOT NULL, read_at TEXT, channel TEXT NOT NULL DEFAULT 'internal',
  UNIQUE(session_id,place_id,notice_id)
);
--> statement-breakpoint
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
  kind TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL
);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS ix_places_session ON places(session_id);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS ix_notices_session ON notices(session_id);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS ix_notifications_session ON notifications(session_id);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS ix_events_session ON events(session_id);
--> statement-breakpoint
CREATE INDEX IF NOT EXISTS ix_sessions_expiry ON sessions(expires_at);
