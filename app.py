from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import requests
import os

# Create the Flask app
app = Flask(__name__)
app.secret_key = "devops-portfolio-secret"  # Simple secret key for sessions

# Database file path
DATABASE = os.path.join(os.path.dirname(__file__), "database", "portfolio.db")

# Change this to your GitHub username to show your real repos
GITHUB_USERNAME = "TejaReddyKuru"

# Hard-coded admin login for simple beginner demo
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def get_db_connection():
    """Return a SQLite connection."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the projects table if it does not exist."""
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                link TEXT NOT NULL
            )
            """
        )
        conn.commit()


def fetch_github_repos():
    """Fetch public repositories from GitHub using the GitHub API."""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        repos = response.json()
        return repos[:6]  # show only first 6 repos for simplicity
    except requests.RequestException:
        return []


def login_required():
    """Simple helper to protect admin pages."""
    if not session.get("logged_in"):
        return redirect(url_for("admin_login"))
    return None


# Initialize the database immediately when the app loads.
# This is easier for beginners and works well for local development.
init_db()


@app.route("/")
def home():
    """Render the home page with skills, projects, and GitHub repos."""
    with get_db_connection() as conn:
        projects = conn.execute("SELECT * FROM projects").fetchall()

    github_repos = fetch_github_repos()
    return render_template("index.html", projects=projects, github_repos=github_repos)


@app.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")


@app.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submission."""
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("home"))

    flash("Thank you for your message! This demo does not send real email.", "success")
    return redirect(url_for("home"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Show login form and validate admin credentials."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            flash("You are now logged in.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Login failed. Use admin/admin123.", "error")
        return redirect(url_for("admin_login"))

    return render_template("login.html")


@app.route("/admin/logout")
def admin_logout():
    """Log out the admin user."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/admin")
def admin_dashboard():
    """Display the admin dashboard with project management."""
    auth = login_required()
    if auth:
        return auth

    with get_db_connection() as conn:
        projects = conn.execute("SELECT * FROM projects").fetchall()
    return render_template("admin_dashboard.html", projects=projects)


@app.route("/admin/add-project", methods=["GET", "POST"])
def add_project():
    """Add a new project to the database."""
    auth = login_required()
    if auth:
        return auth

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        link = request.form.get("link")

        if not title or not description or not link:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("add_project"))

        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO projects (title, description, link) VALUES (?, ?, ?)",
                (title, description, link),
            )
            conn.commit()

        flash("Project added successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_project.html")


@app.route("/admin/edit-project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    """Edit an existing project."""
    auth = login_required()
    if auth:
        return auth

    with get_db_connection() as conn:
        project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

    if project is None:
        flash("Project not found.", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        link = request.form.get("link")

        if not title or not description or not link:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("edit_project", project_id=project_id))

        with get_db_connection() as conn:
            conn.execute(
                "UPDATE projects SET title = ?, description = ?, link = ? WHERE id = ?",
                (title, description, link, project_id),
            )
            conn.commit()

        flash("Project updated successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("edit_project.html", project=project)


@app.route("/admin/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    """Delete a project from the database."""
    auth = login_required()
    if auth:
        return auth

    with get_db_connection() as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()

    flash("Project deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    # Run the app locally on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
