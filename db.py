"""
SpamShield AI - SQLite Persistence Layer
Handles storage, retrieval, and management of detection history and contact messages.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "spamshield.db")


def get_db_connection():
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables if they do not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message TEXT NOT NULL,
                message_preview TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                spam_probability REAL NOT NULL,
                normal_probability REAL NOT NULL,
                reasons_json TEXT,
                patterns_json TEXT,
                links_json TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL
            );
        """)
        conn.commit()


def save_detection(data: Dict[str, Any], full_message: str) -> int:
    """Saves a detection result into SQLite history."""
    preview = full_message.strip().replace("\n", " ")
    if len(preview) > 100:
        preview = preview[:97] + "..."

    reasons_json = json.dumps(data.get("reasons", []))
    patterns_json = json.dumps(data.get("patterns_detected", []))
    links_json = json.dumps(data.get("links_found", []))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO detection_history (
                message, message_preview, prediction, confidence,
                spam_probability, normal_probability,
                reasons_json, patterns_json, links_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            full_message,
            preview,
            data.get("prediction", "UNKNOWN"),
            data.get("confidence", 0.0),
            data.get("spam_probability", 0.0),
            data.get("normal_probability", 0.0),
            reasons_json,
            patterns_json,
            links_json
        ))
        conn.commit()
        return cursor.lastrowid


def get_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent detection history."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, message, message_preview, prediction,
                   confidence, spam_probability, normal_probability,
                   reasons_json, patterns_json, links_json
            FROM detection_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        history = []
        for row in rows:
            history.append({
                "id": row["id"],
                "created_at": row["created_at"],
                "message": row["message"],
                "message_preview": row["message_preview"],
                "prediction": row["prediction"],
                "confidence": row["confidence"],
                "spam_probability": row["spam_probability"],
                "normal_probability": row["normal_probability"],
                "reasons": json.loads(row["reasons_json"] or "[]"),
                "patterns_detected": json.loads(row["patterns_json"] or "[]"),
                "links_found": json.loads(row["links_json"] or "[]")
            })
        return history


def get_history_item(item_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves a single detection history item."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, message, message_preview, prediction,
                   confidence, spam_probability, normal_probability,
                   reasons_json, patterns_json, links_json
            FROM detection_history
            WHERE id = ?
        """, (item_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "created_at": row["created_at"],
            "message": row["message"],
            "message_preview": row["message_preview"],
            "prediction": row["prediction"],
            "confidence": row["confidence"],
            "spam_probability": row["spam_probability"],
            "normal_probability": row["normal_probability"],
            "reasons": json.loads(row["reasons_json"] or "[]"),
            "patterns_detected": json.loads(row["patterns_json"] or "[]"),
            "links_found": json.loads(row["links_json"] or "[]")
        }


def delete_history_item(item_id: int) -> bool:
    """Deletes a single history record."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM detection_history WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_all_history() -> bool:
    """Clears all detection records from database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM detection_history")
        conn.commit()
        return True


def save_contact(name: str, email: str, subject: str, message: str) -> int:
    """Saves user contact form submission."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_submissions (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        """, (name, email, subject, message))
        conn.commit()
        return cursor.lastrowid


def get_stats() -> Dict[str, Any]:
    """Computes aggregate detection statistics."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM detection_history")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM detection_history WHERE prediction = 'SPAM'")
        spam_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM detection_history WHERE prediction = 'NORMAL'")
        normal_count = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(confidence) FROM detection_history")
        avg_conf = cursor.fetchone()[0] or 0.0

        return {
            "total_analyzed": total,
            "spam_count": spam_count,
            "normal_count": normal_count,
            "avg_confidence": round(avg_conf, 1)
        }
