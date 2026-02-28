import streamlit as st
import json
import os
from datetime import datetime

# Users database file
USERS_DB = "users_db.json"

# Load or create users database
def load_users():
    if os.path.exists(USERS_DB):
        with open(USERS_DB, 'r') as f:
            return json.load(f)
    return {}

# Save users database
def save_users(users):
    with open(USERS_DB, 'w') as f:
        json.dump(users, f, indent=4)

# Register new user
def register_user(email, password, full_name):
    users = load_users()
    
    if email in users:
        return False, "Email already registered"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    users[email] = {
        "password": password,
        "full_name": full_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "analyses": 0
    }
    
    save_users(users)
    return True, "Registration successful! Please login."

# Login user
def login_user(email, password):
    users = load_users()
    
    # auto-create demo account if it doesn't exist
    if email == "demo@example.com" and email not in users:
        users[email] = {
            "password": password,
            "full_name": "Demo User",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analyses": 0
        }
        save_users(users)
    
    if email not in users:
        return False, "Email not found"
    
    if users[email]["password"] != password:
        return False, "Incorrect password"
    
    return True, users[email]["full_name"]

# Get user info
def get_user_info(email):
    users = load_users()
    if email in users:
        return users[email]
    return None

# Update user analyses count
def increment_analyses(email):
    users = load_users()
    if email in users:
        users[email]["analyses"] = users[email].get("analyses", 0) + 1
        save_users(users)
