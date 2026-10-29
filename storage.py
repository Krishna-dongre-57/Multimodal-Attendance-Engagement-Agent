import sqlite3

DB_NAME = "data/session.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        present INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS engagement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score REAL,
        level TEXT,
        recommendation TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_attendance(student_id, present):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO attendance
        (student_id, present)
        VALUES (?, ?)
        """,
        (student_id, present)
    )

    conn.commit()
    conn.close()


def save_engagement(
    score,
    level,
    recommendation
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO engagement
        (score, level, recommendation)
        VALUES (?, ?, ?)
        """,
        (score, level, recommendation)
    )

    conn.commit()
    conn.close()


def get_present_student_count():
    conn = sqlite3.connect(DB_NAME)

    try:
        cursor = conn.execute(
            """
            SELECT COUNT(DISTINCT student_id)
            FROM attendance
            WHERE present = 1
            """
        )
        return cursor.fetchone()[0]
    finally:
        conn.close()


def get_recent_engagement(limit=30):
    conn = sqlite3.connect(DB_NAME)

    try:
        cursor = conn.execute(
            """
            SELECT score, level, recommendation, timestamp
            FROM (
                SELECT id, score, level, recommendation, timestamp
                FROM engagement
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
            """,
            (max(1, int(limit)),)
        )
        return [
            {
                "score": row[0],
                "level": row[1],
                "recommendation": row[2],
                "timestamp": row[3]
            }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()