import sqlite3


class DatabaseRepository:

    MAX_NAME_LEN = 256
    MAX_MESSAGE_LEN = 8096

    def __init__(self, db_path: str = ":memory:"):

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row # строки как словари а не кортежи 
        self._create_table()

    def _create_table(self):
        # Создаём таблицу, если её ещё нет
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id      INTEGER PRIMARY KEY,
                name    TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        self.conn.commit()

    # Валидация
    def _validate(self, comment_id, username, message):
        if not isinstance(comment_id, int) or comment_id <= 0:
            raise ValueError("id должен быть положительным целым числом")
        if not isinstance(username, str) or not username.strip():
            raise ValueError("name должен быть непустой строкой")
        if len(username) > self.MAX_NAME_LEN:
            raise ValueError(f"name длиннее {self.MAX_NAME_LEN} символов")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("message должен быть непустой строкой")
        if len(message) > self.MAX_MESSAGE_LEN:
            raise ValueError(f"message длиннее {self.MAX_MESSAGE_LEN} символов")

    # CRUD
    def add(self, comment_id: int, username: str, message: str) -> bool:
        """Добавить запись. Бросает ValueError при невалидных данных,
        sqlite3.IntegrityError при дублировании id."""
        self._validate(comment_id, username, message)
        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # дубликат id — пробрасываем наверх, тест это проверит
            raise

    def get_by_id(self, comment_id: int):
        """Вернуть запись как dict или None."""
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE id = ?",
            (comment_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str):
        """Вернуть список всех записей пользователя."""
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE name = ?",
            (username,),
        )
        return [dict(r) for r in cur.fetchall()]

    def update(self, comment_id: int, new_message: str) -> bool:
        """Обновить message по id. Бросает ValueError при невалидной длине
        или LookupError, если записи с таким id нет."""
        if not isinstance(new_message, str) or not new_message.strip():
            raise ValueError("message должен быть непустой строкой")
        if len(new_message) > self.MAX_MESSAGE_LEN:
            raise ValueError(f"message длиннее {self.MAX_MESSAGE_LEN} символов")

        cur = self.conn.execute(
            "UPDATE comments SET message = ? WHERE id = ?",
            (new_message, comment_id),
        )
        self.conn.commit()
        if cur.rowcount == 0:
            raise LookupError(f"Запись с id={comment_id} не найдена")
        return True

    def delete(self, comment_id: int) -> bool:
        """Удалить запись по id. Возвращает True, если что-то удалено."""
        cur = self.conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()