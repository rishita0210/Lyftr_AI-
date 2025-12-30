from datetime import datetime
import sqlite3
from app.models import get_connection


def insert_message(message):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO messages (
                message_id,
                from_msisdn,
                to_msisdn,
                ts,
                text,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            message.message_id,
            message.from_msisdn,
            message.to_msisdn,
            message.ts.isoformat().replace("+00:00", "Z"),
            message.text,
            datetime.utcnow().isoformat() + "Z"
        ))

        conn.commit()
        return "created"

    except sqlite3.IntegrityError:
        # Duplicate message_id
        return "duplicate"

    finally:
        conn.close()
