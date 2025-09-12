import os
import sqlite3
from typing import Optional, Any, Dict
from contextlib import contextmanager
from constants import DB_NAME

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(SCRIPT_DIR, "..", "database", DB_NAME)

class OperationResult:
    def __init__(
            self, success: bool, 
            data: Optional[Any] = None, message: Optional[str] = None):
        self.success = success
        self.data = data
        self.message = message

    def __bool__(self):
        return self.success

    def __repr__(self):
        return f"OperationResult(success={self.success}, \
            data={self.data}, message=\'{self.message}\')"


class VocabularyDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = DB_NAME
        self.db_path = db_path
        self.init_database()

        # Сaching the maximum length of words
        self._max_widths = self._calculate_max_widths()
        self._num_of_entries = self._calculate_num_of_entries()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS dict (
                        uniq_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                        english  TEXT,
                        otherlg  TEXT,  --other language you use
                        context  TEXT
                    );
                    """
                )
                conn.commit()
            return OperationResult(
                success=True, message="Database initialized successfully.")
        except sqlite3.Error as e:
            return OperationResult(
                success=False, message=f"Database initialization failed: {e}")

    # Calculates the maximum word lengths for formatting (caching)
    def _calculate_max_widths(self) -> Dict[str, int]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT 
                        MAX(LENGTH(english)) as max_eng,
                        MAX(LENGTH(otherlg)) as max_rus
                    FROM dict
                    """
                )
                result = cursor.fetchone()
                return { 
                    "english": result["max_eng"] or 10,
                    "russian": result["max_rus"] or 10
                    }
        except sqlite3.Error:
            return {"english": 10, "russian": 10}  # fallback values

    def get_max_widths(self) -> Dict[str, int]:
        return self._max_widths.copy()

    # Updates the cache if new words are longer than the current maximum
    def invalidate_width_cache(self):
        self._max_widths = self._calculate_max_widths()

    def add_word(
            self, english: str, otherlg: str, context: str = None) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Check if word already exists
                cursor.execute(
                    """
                    SELECT 1 FROM dict 
                    WHERE english = ?
                    """,
                    (english,)
                )
                if cursor.fetchone():
                    return OperationResult(
                        success=False, message="Word already exists")

                cursor.execute(
                    """
                    INSERT INTO dict (english, otherlg, context) 
                    VALUES (?, ?, ?)
                    """,
                    (english, otherlg, context),
                )
                conn.commit()

                # Update the cache if new words are longer than the current maximum
                if (
                    len(english) > self._max_widths["english"]
                    or len(otherlg) > self._max_widths["russian"]
                ):
                    self.invalidate_width_cache()
                self.invalidate_num_of_entries_cache()

                return OperationResult(success=True, message="Word added successfully")
        except sqlite3.Error as e:
            return OperationResult(success=False, message=f"Failed to add word: {e}")

    def edit_word(self, english: str, new_otherlg: Optional[str] = None, 
                  new_context: Optional[str] = None) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                updates = []
                params = []
                if new_otherlg is not None:
                    updates.append("otherlg = ?")
                    params.append(new_otherlg)
                if new_context is not None:
                    updates.append("context = ?")
                    params.append(new_context)
                
                if not updates:
                    return OperationResult(
                        success=False, message="No new values provided for update.")

                sql = f"UPDATE dict SET {', '.join(updates)} WHERE english = ?"
                params.append(english)

                cursor.execute(sql, tuple(params))
                conn.commit()

                if cursor.rowcount > 0:
                    self.invalidate_width_cache()
                    return OperationResult(
                        success=True, message=f"Word '{english}' updated successfully.")
                else:
                    return OperationResult(
                        success=False, message=f"Word '{english}' not found.")
        except sqlite3.Error as e:
            return OperationResult(
                success=False, message=f"Failed to update word '{english}': {e}")

    def delete_word(self, english: str) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    DELETE FROM dict WHERE english = ?
                    """,
                    (english,),
                )
                conn.commit()
                self.invalidate_num_of_entries_cache()
                if cursor.rowcount > 0:
                    return OperationResult(
                        success=True, message=f"Word \'{english}\' deleted successfully.")
                else:
                    return OperationResult(
                        success=False, message=f"Word \'{english}\' not found.")
        except sqlite3.Error as e:
            return OperationResult(
                success=False, message=f"Failed to delete word \'{english}\': {e}")

    # Calculates the number of entries (caching)
    def _calculate_num_of_entries(self) -> int:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM dict")
                result = cursor.fetchone()
                return result[0]
        except sqlite3.Error:
            return 0

    # Returns cached number of entries
    def get_num_of_entries(self) -> int:
        return self._num_of_entries

    # Updates the cache after data changes
    def invalidate_num_of_entries_cache(self):
        self._num_of_entries = self._calculate_num_of_entries()

    def get_word(self, english: str) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT english, otherlg, context
                    FROM dict
                    WHERE english = ?
                    """,
                    (english,),
                )
                row = cursor.fetchone()
                if row:
                    return OperationResult(
                        success=True,
                        data=dict(row),
                        message=f"Word \'{english}\' retrieved successfully.",)
                else:
                    return OperationResult(
                        success=False, message=f"Word \'{english}\' not found.")
        except sqlite3.Error as e:
            return OperationResult(
                success=False, message=f"Failed to retrieve word \'{english}\': {e}")

    def get_all_words(self) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT english, otherlg, context 
                    FROM dict
                    ORDER by english;
                    """
                )
                words = [dict(row) for row in cursor.fetchall()]
                return OperationResult(
                    success=True,
                    data=words,
                    message="All words retrieved successfully.",)
        except sqlite3.Error as e:
            return OperationResult(
                success=False, message=f"Failed to retrieve all words: {e}")

    def search_words(self, prefix: str) -> OperationResult:
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT uniq_id,
                        english,
                        otherlg,
                        context
                    FROM dict
                    WHERE english LIKE ? COLLATE NOCASE
                    ORDER BY english COLLATE NOCASE
                    """,
                    (f"{prefix}%",),
                )
                columns = [col[0] for col in cur.description]
                words = [dict(zip(columns, row)) for row in cur.fetchall()]
                return OperationResult(
                    success=True,
                    data=words,
                    message=f"Words with prefix \'{prefix}\' searched successfully.",)
        except sqlite3.Error as e:
            return OperationResult(
                success=False,
                message=f"Failed to search words with prefix \'{prefix}\': {e}",)


