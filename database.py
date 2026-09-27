"""
database.py - SQLite Database Layer for Anwar's Cinematic Portfolio
Preserves all existing portfolio information and provides dynamic content management.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Profile Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        full_name TEXT NOT NULL,
        title TEXT NOT NULL,
        bio TEXT NOT NULL,
        email TEXT,
        location TEXT,
        resume_url TEXT,
        photo_url TEXT,
        hero_cta TEXT,
        hero_cta_link TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Skills Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT DEFAULT 'Development',
        proficiency INTEGER DEFAULT 80,
        icon TEXT,
        display_order INTEGER DEFAULT 0
    )
    """)

    # 3. Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        technologies TEXT,
        image_url TEXT,
        github_url TEXT,
        live_url TEXT,
        status TEXT DEFAULT 'Completed',
        display_order INTEGER DEFAULT 0
    )
    """)

    # 4. Experience Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS experience (
        experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        description TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        display_order INTEGER DEFAULT 0
    )
    """)

    # 5. Education Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS education (
        education_id INTEGER PRIMARY KEY AUTOINCREMENT,
        institution TEXT NOT NULL,
        degree TEXT NOT NULL,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        display_order INTEGER DEFAULT 0
    )
    """)

    # 6. Contact Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 7. Cinematic Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cinematic_settings (
        setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        animation_name TEXT NOT NULL,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT NOT NULL,
        description TEXT,
        enabled INTEGER DEFAULT 1
    )
    """)

    # 8. Admin Users Table (Default credentials: admin / anwar2026)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed Initial Data if empty (PRESERVING EXACT EXISTING PORTFOLIO DATA)
    # Check Profile
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO profile (name, full_name, title, bio, email, location, resume_url, photo_url, hero_cta, hero_cta_link)
        VALUES (
            'Anwar',
            'Anwar Hussain',
            'Python Full Stack Developer in training',
            'I started learning Python to become a Full Stack Developer. I love building things that live on the internet.',
            'anwar.hussain@example.com',
            'Global / Remote',
            '#',
            '/static/images/anwar.jpeg',
            'Hire me',
            '#contact'
        )
        """)

    # Check Skills (Preserving exact items from skills.html)
    cursor.execute("SELECT COUNT(*) FROM skills")
    if cursor.fetchone()[0] == 0:
        skills_data = [
            ("Python", "Backend", 88, "fa-brands fa-python", 1),
            ("Flask", "Backend Framework", 82, "fa-solid fa-pepper-hot", 2),
            ("HTML & CSS", "Frontend", 85, "fa-brands fa-html5", 3),
            ("Javascript", "Frontend & Interactive", 75, "fa-brands fa-js", 4),
            ("SQL(Coming soon)", "Database & Architecture", 50, "fa-solid fa-database", 5)
        ]
        cursor.executemany("""
        INSERT INTO skills (name, category, proficiency, icon, display_order)
        VALUES (?, ?, ?, ?, ?)
        """, skills_data)

    # Check Projects (Preserving exact items from projects.html)
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        projects_data = [
            (
                "Portfolio Website",
                "A personal portfolio built with Flask and jinja2 templates.",
                "Python, Flask, Jinja2, CSS3, GSAP",
                "",
                "#",
                "#",
                "Completed",
                1
            ),
            (
                "Task manager(comming soon)",
                "Full CRUD app with database and user login.",
                "Python, Flask, SQLite, Authentication",
                "",
                "#",
                "#",
                "In Progress",
                2
            )
        ]
        cursor.executemany("""
        INSERT INTO projects (title, description, technologies, image_url, github_url, live_url, status, display_order)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, projects_data)

    # Check Experience
    cursor.execute("SELECT COUNT(*) FROM experience")
    if cursor.fetchone()[0] == 0:
        exp_data = [
            (
                "Independent Practice & Projects",
                "Python Full Stack Developer in Training",
                "Designing web applications with Flask, Jinja2, SQL databases, and modern interactive UI architectures.",
                "2025",
                "Present",
                1
            )
        ]
        cursor.executemany("""
        INSERT INTO experience (company, role, description, start_date, end_date, display_order)
        VALUES (?, ?, ?, ?, ?, ?)
        """, exp_data)

    # Check Education
    cursor.execute("SELECT COUNT(*) FROM education")
    if cursor.fetchone()[0] == 0:
        edu_data = [
            (
                "Academic / Self-Paced Curriculum",
                "Full Stack Web Development & Computer Science",
                "Comprehensive study of Python, algorithms, web servers, frontend fundamentals, and database engineering.",
                "2023",
                "2026",
                1
            )
        ]
        cursor.executemany("""
        INSERT INTO education (institution, degree, description, start_date, end_date, display_order)
        VALUES (?, ?, ?, ?, ?, ?)
        """, edu_data)

    # Check Cinematic Settings
    cursor.execute("SELECT COUNT(*) FROM cinematic_settings")
    if cursor.fetchone()[0] == 0:
        settings_data = [
            ("Cat Scroll Timeline", "cat_animation_enabled", "1", "Controls scroll-linked cat character transitions", 1),
            ("Atmospheric Mist & Particles", "particles_enabled", "1", "Renders subtle floating blue dust and fog canvas", 1),
            ("Cat Eye Glow Color", "eye_glow_color", "#38bdf8", "Electric-blue cyan eye luminescence", 1),
            ("Smooth Scroll Feel", "smooth_scroll", "1", "Enables cinematic eased scrolling transitions", 1),
            ("Ambient Sound FX", "ambient_sound", "0", "Optional subtle atmospheric audio hum (muted by default)", 0)
        ]
        cursor.executemany("""
        INSERT INTO cinematic_settings (animation_name, setting_key, setting_value, description, enabled)
        VALUES (?, ?, ?, ?, ?)
        """, settings_data)

    # Check Admin User
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    if cursor.fetchone()[0] == 0:
        # Default simple admin credentials (can be updated from dashboard)
        import hashlib
        default_pass = hashlib.sha256("anwar2026".encode("utf-8")).hexdigest()
        cursor.execute("INSERT INTO admin_users (username, password_hash) VALUES ('admin', ?)", (default_pass,))

    conn.commit()
    conn.close()

# Helper Query Functions

def get_portfolio_data():
    """Fetch all dynamic content needed for the portfolio page."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profile ORDER BY id DESC LIMIT 1")
    profile = cursor.fetchone()

    cursor.execute("SELECT * FROM skills ORDER BY display_order ASC, skill_id ASC")
    skills = cursor.fetchall()

    cursor.execute("SELECT * FROM projects ORDER BY display_order ASC, project_id ASC")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM experience ORDER BY display_order ASC, experience_id ASC")
    experience = cursor.fetchall()

    cursor.execute("SELECT * FROM education ORDER BY display_order ASC, education_id ASC")
    education = cursor.fetchall()

    cursor.execute("SELECT * FROM cinematic_settings")
    settings_rows = cursor.fetchall()
    settings = {row['setting_key']: row['setting_value'] for row in settings_rows}

    conn.close()
    return {
        "profile": dict(profile) if profile else {},
        "skills": [dict(s) for s in skills],
        "projects": [dict(p) for p in projects],
        "experience": [dict(e) for e in experience],
        "education": [dict(ed) for ed in education],
        "settings": settings
    }

def save_contact_message(name, email, message):
    """Save an incoming contact message into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO contact_messages (name, email, message)
    VALUES (?, ?, ?)
    """, (name, email, message))
    conn.commit()
    conn.close()

def get_all_messages():
    """Retrieve all contact messages for the admin."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    messages = cursor.fetchall()
    conn.close()
    return [dict(m) for m in messages]

def verify_admin_login(username, password):
    """Verify admin login credentials."""
    import hashlib
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_users WHERE username = ? AND password_hash = ?", (username, pw_hash))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def update_profile_data(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE profile SET
        name = ?,
        full_name = ?,
        title = ?,
        bio = ?,
        email = ?,
        location = ?,
        resume_url = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = 1
    """, (
        data.get("name"),
        data.get("full_name"),
        data.get("title"),
        data.get("bio"),
        data.get("email"),
        data.get("location"),
        data.get("resume_url")
    ))
    conn.commit()
    conn.close()

def add_skill(name, category, proficiency, display_order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO skills (name, category, proficiency, display_order)
    VALUES (?, ?, ?, ?)
    """, (name, category, proficiency, display_order))
    conn.commit()
    conn.close()

def delete_skill(skill_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM skills WHERE skill_id = ?", (skill_id,))
    conn.commit()
    conn.close()

def add_project(title, description, technologies, github_url, live_url, status, display_order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO projects (title, description, technologies, github_url, live_url, status, display_order)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, technologies, github_url, live_url, status, display_order))
    conn.commit()
    conn.close()

def delete_project(project_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()

def update_cinematic_setting(setting_key, setting_value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE cinematic_settings SET setting_value = ? WHERE setting_key = ?
    """, (setting_value, setting_key))
    conn.commit()
    conn.close()
