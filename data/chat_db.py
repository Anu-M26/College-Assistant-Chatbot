"""
Database module for storing chat history
This file helps save and retrieve student conversations from SQLite database
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Get the directory where this file is located
DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "chatbot.db"


def init_database():
    """
    Create the database and chat history table if they don't exist
    This is called when the app starts for the first time
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            question TEXT,
            answer TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    connection.commit()
    connection.close()


def save_chat(student_name, question, answer):
    """
    Save a question and answer to the database
    
    Args:
        student_name: Name of the student asking the question
        question: The student's question
        answer: The chatbot's response
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO chat_history (student_name, question, answer, timestamp)
        VALUES (?, ?, ?, ?)
    """, (student_name, question, answer, datetime.now()))
    
    connection.commit()
    connection.close()


def get_chat_history(student_name, limit=10):
    """
    Retrieve chat history for a specific student
    
    Args:
        student_name: Name of the student
        limit: Maximum number of messages to retrieve (default: 10)
    
    Returns:
        List of dictionaries containing question, answer, and timestamp
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT question, answer, timestamp 
        FROM chat_history 
        WHERE student_name = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (student_name, limit))
    
    rows = cursor.fetchall()
    connection.close()
    
    # Convert rows to list of dictionaries
    history = []
    for row in rows:
        history.append({
            "question": row[0],
            "answer": row[1],
            "timestamp": row[2]
        })
    
    return history
