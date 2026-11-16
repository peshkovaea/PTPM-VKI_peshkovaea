import sqlite3

class DatabaseRepository:
    MAX_NAME_LEN = 256
    MAX_MESSAGE_LEN = 8096

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # позволяет получать данные как словари
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id      INTEGER PRIMARY KEY,
                name    TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def _validate(self, comment_id, username, message):
        # Валидация типов и длины
        if not isinstance(comment_id, int) or comment_id <= 0:
            raise ValueError("ID должен быть положительным целым числом")
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя (name) должно быть непустой строкой")
        if len(username) > self.MAX_NAME_LEN:
            raise ValueError(f"Имя длиннее {self.MAX_NAME_LEN} символов")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Сообщение (message) должно быть непустой строкой")
        if len(message) > self.MAX_MESSAGE_LEN:
            raise ValueError(f"Сообщение длиннее {self.MAX_MESSAGE_LEN} символов")

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._validate(comment_id, username, message)
        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Выбросит ошибку при дублировании ID 
            raise 

    def get_by_id(self, comment_id: int):
        cur = self.conn.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str):
        cur = self.conn.execute("SELECT * FROM comments WHERE name = ?", (username,))
        return [dict(r) for r in cur.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        if not isinstance(new_message, str) or not new_message.strip():
            raise ValueError("Сообщение должно быть непустой строкой")
        if len(new_message) > self.MAX_MESSAGE_LEN:
            raise ValueError(f"Сообщение длиннее {self.MAX_MESSAGE_LEN} символов")

        cur = self.conn.execute("UPDATE comments SET message = ? WHERE id = ?", (new_message, comment_id))
        self.conn.commit()
        
        if cur.rowcount == 0:
            raise LookupError(f"Запись с ID={comment_id} не найдена")
        return True

    def delete(self, comment_id: int) -> bool:
        # Нужен для тестов
        cur = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()