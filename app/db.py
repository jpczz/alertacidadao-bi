"""Transactional repository: SQLite locally or PostgreSQL via DATABASE_URL.

The SQL used by the application is deliberately shared between both engines.
Connection URLs are never returned by the API or included in evidence exports.
"""
import json, sqlite3
from pathlib import Path
from contextlib import contextmanager

SCHEMA='''
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS sessions (
 id TEXT PRIMARY KEY, csrf TEXT NOT NULL, created_at TEXT NOT NULL, expires_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS places (
 id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
 label TEXT NOT NULL, street TEXT NOT NULL, number TEXT NOT NULL, neighborhood TEXT NOT NULL,
 city TEXT NOT NULL, state TEXT NOT NULL, postal_code TEXT NOT NULL, zone TEXT NOT NULL,
 chuva INTEGER NOT NULL, calor INTEGER NOT NULL, consent INTEGER NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS notices (
 id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
 code TEXT NOT NULL, version INTEGER NOT NULL, payload TEXT NOT NULL, created_at TEXT NOT NULL,
 UNIQUE(session_id,code,version)
);
CREATE TABLE IF NOT EXISTS notifications (
 id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
 place_id TEXT NOT NULL REFERENCES places(id) ON DELETE CASCADE,
 notice_id TEXT NOT NULL REFERENCES notices(id) ON DELETE CASCADE,
 created_at TEXT NOT NULL, read_at TEXT, channel TEXT NOT NULL DEFAULT 'internal',
 UNIQUE(session_id,place_id,notice_id)
);
CREATE TABLE IF NOT EXISTS events (
 id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
 kind TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_places_session ON places(session_id);
CREATE INDEX IF NOT EXISTS ix_notices_session ON notices(session_id);
CREATE INDEX IF NOT EXISTS ix_notifications_session ON notifications(session_id);
CREATE INDEX IF NOT EXISTS ix_events_session ON events(session_id);
'''

POSTGRES_SCHEMA=SCHEMA.replace('PRAGMA foreign_keys=ON;', '').replace(
    'id INTEGER PRIMARY KEY AUTOINCREMENT', 'id BIGSERIAL PRIMARY KEY'
)

class _PostgresRow(dict):
    """Keep sqlite.Row's key and positional lookup interface for our queries."""
    def __getitem__(self,key):
        if isinstance(key,int):
            return tuple(self.values())[key]
        return super().__getitem__(key)

def _postgres_row_factory(cursor):
    names=[column.name for column in cursor.description] if cursor.description else []
    return lambda values: _PostgresRow(zip(names,values))

class _PostgresConnection:
    def __init__(self,connection):
        self.connection=connection

    def execute(self,sql,args=()):
        # Only application-owned SQL reaches here. Values remain bound parameters.
        return self.connection.execute(sql.replace('?', '%s'),args)

class Store:
    def __init__(self,path: str):
        self.path=path
        self.backend='postgresql' if path.startswith(('postgresql://','postgres://')) else 'sqlite'
        if self.backend=='postgresql':
            with self._postgres_connect() as con:
                for statement in POSTGRES_SCHEMA.split(';'):
                    if statement.strip():
                        con.execute(statement)
            return
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        con=sqlite3.connect(self.path,timeout=15,isolation_level=None)
        try:
            con.execute('PRAGMA journal_mode=WAL')
            con.executescript(SCHEMA)
        finally:
            con.close()

    def _postgres_connect(self):
        import psycopg
        return psycopg.connect(
            self.path,connect_timeout=10,row_factory=_postgres_row_factory,
            options='-c statement_timeout=15000 -c lock_timeout=10000',
        )

    @contextmanager
    def connect(self):
        if self.backend=='postgresql':
            # psycopg's context manager commits on success, rolls back on failure,
            # and always closes the connection, including exceptions in handlers.
            with self._postgres_connect() as con:
                yield _PostgresConnection(con)
            return
        con=sqlite3.connect(self.path,timeout=15,isolation_level=None)
        con.row_factory=sqlite3.Row
        con.execute('PRAGMA foreign_keys=ON')
        try:
            con.execute('BEGIN IMMEDIATE')
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally: con.close()

    def event(self,con,sid,kind,detail,now):
        con.execute('INSERT INTO events(session_id,kind,detail,created_at) VALUES (?,?,?,?)',(sid,kind,json.dumps(detail,ensure_ascii=False),now))

    @staticmethod
    def rows(con,sql,args=()):
        return [dict(row) for row in con.execute(sql,args).fetchall()]
