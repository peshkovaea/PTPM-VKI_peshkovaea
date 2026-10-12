import sqlite3

class TriangleDB:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL, b REAL, c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()

    def add(self, a, b, c, t_type, err):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (a, b, c, t_type, err),
        )
        self.conn.commit()

    def get(self, a, b, c):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles WHERE a=? AND b=? AND c=?",
            (a, b, c),
        )
        return cur.fetchone()  # None, если нет записи

    def delete(self, a, b, c):
        self.conn.execute("DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        self.conn.commit()