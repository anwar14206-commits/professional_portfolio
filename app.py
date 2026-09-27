"""
app.py - Anwar Hussain's Cinematic Portfolio Web Application
Centered around the mysterious black cat journey, powered by Flask & SQLite.
"""

from flask import Flask, redirect, render_template, request, flash, url_for, jsonify, session
import os
import database

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "portfolio_secret_key_2026")

# Initialize database on startup
database.init_db()

# ===================================================================
# PUBLIC PORTFOLIO ROUTES (Preserved URLs & Content)
# ===================================================================

@app.route("/")
@app.route("/home")
def home():
    """Master Cinematic Portfolio Experience with Black Cat Guided Journey"""
    data = database.get_portfolio_data()
    return render_template("index.html", **data)

@app.route("/about")
def about():
    """Preserved About route"""
    data = database.get_portfolio_data()
    return render_template("about.html", **data)

@app.route("/skills")
def skills():
    """Preserved Skills route"""
    data = database.get_portfolio_data()
    return render_template("skills.html", **data)

@app.route("/projects")
def projects():
    """Preserved Projects route"""
    data = database.get_portfolio_data()
    return render_template("projects.html", **data)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Preserved Contact route with database persistence and AJAX support"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if name and email and message:
            # Save to Database
            database.save_contact_message(name, email, message)

        success_msg = f"Thank you {name}! Your message been sent."
        flash(success_msg, "success")

        # Support seamless AJAX transmission without page refresh
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "status": "success",
                "message": success_msg
            })

        return redirect(url_for("home"))

    data = database.get_portfolio_data()
    return render_template("contact.html", **data)

# ===================================================================
# SECURE ADMIN CMS ROUTES
# ===================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if database.verify_admin_login(username, password):
            session["admin_logged_in"] = True
            session["admin_user"] = username
            flash("Welcome to Sanctuary Admin Control.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid administrator credentials. Access denied.", "danger")

    return render_template("admin/login.html")

@app.route("/admin")
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    data = database.get_portfolio_data()
    messages = database.get_all_messages()
    return render_template("admin/dashboard.html", messages=messages, **data)

@app.route("/admin/profile/update", methods=["POST"])
def admin_update_profile():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    profile_data = {
        "name": request.form.get("name"),
        "full_name": request.form.get("full_name"),
        "title": request.form.get("title"),
        "bio": request.form.get("bio"),
        "email": request.form.get("email"),
        "location": request.form.get("location"),
        "resume_url": request.form.get("resume_url", "#")
    }
    database.update_profile_data(profile_data)
    flash("Profile narrative updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/skills/add", methods=["POST"])
def admin_add_skill():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    name = request.form.get("name")
    category = request.form.get("category", "Development")
    proficiency = int(request.form.get("proficiency", 80))
    display_order = int(request.form.get("display_order", 0))

    if name:
        database.add_skill(name, category, proficiency, display_order)
        flash(f"Skill '{name}' added successfully.", "success")

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/skills/delete/<int:skill_id>", methods=["POST"])
def admin_delete_skill(skill_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    database.delete_skill(skill_id)
    flash("Skill removed from portfolio.", "info")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/projects/add", methods=["POST"])
def admin_add_project():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    title = request.form.get("title")
    description = request.form.get("description")
    technologies = request.form.get("technologies")
    github_url = request.form.get("github_url", "#")
    live_url = request.form.get("live_url", "#")
    status = request.form.get("status", "Completed")
    display_order = int(request.form.get("display_order", 0))

    if title and description:
        database.add_project(title, description, technologies, github_url, live_url, status, display_order)
        flash(f"Project '{title}' created.", "success")

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/projects/delete/<int:project_id>", methods=["POST"])
def admin_delete_project(project_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    database.delete_project(project_id)
    flash("Project deleted.", "info")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/settings/update", methods=["POST"])
def admin_update_settings():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    for key in ["cat_animation_enabled", "particles_enabled", "eye_glow_color", "smooth_scroll"]:
        val = request.form.get(key)
        if val is not None:
            database.update_cinematic_setting(key, val)

    flash("Cinematic settings updated.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_user", None)
    flash("You have safely logged out of Sanctuary Admin.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)