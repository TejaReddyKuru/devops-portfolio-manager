# DevOps Portfolio Manager

A beginner-friendly local portfolio website built with:
- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite
- DevOps: Docker and GitHub Actions

This project helps you learn GitHub workflow, folder structure, Docker basics, CI/CD basics, and a simple backend/frontend connection.

## Folder Structure

```
project/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── add_project.html
│   └── edit_project.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── database/
│   └── portfolio.db  # created automatically
├── tests/
│   └── test_app.py
└── README.md
```

## Setup Instructions

### 1. Run locally with Python

1. Open your terminal in the project folder.
2. Create a Python virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the app:
   ```powershell
   python app.py
   ```
5. Open your browser at `http://localhost:5000`

### 2. Run with Docker

1. Build and start the containers:
   ```powershell
   docker compose up --build
   ```
2. Open your browser at `http://localhost:5000`

### 3. Run tests

```powershell
python -m unittest discover -s tests
```

## How to Use the App

- Home page: shows a welcome section, skills, projects, contact form, and GitHub repositories.
- About page: shares a short introduction.
- Admin login: go to `/admin/login` and use `admin` / `admin123`.
- Add/Edit/Delete projects: manage project cards from the admin dashboard.

## Docker Files

- `Dockerfile`: defines a Python container image for the Flask app.
- `docker-compose.yml`: starts the `web` service and forwards port 5000.

## GitHub Actions

- `.github/workflows/ci.yml`: runs on push and pull request.
- Steps:
  1. Checkout code
  2. Install dependencies
  3. Run tests
  4. Build Docker image

## Simple Explanations for Viva / Interviews

### What is Docker?
Docker is a tool that puts applications inside small virtual packages called containers. Containers let your app run the same way on any computer.

### What is CI/CD?
CI/CD stands for Continuous Integration and Continuous Delivery. It means automatically testing and building code whenever someone changes it.

### What is GitHub Actions?
GitHub Actions is a service that runs tasks automatically for your code. It can test your app, build Docker images, and help deploy changes.

### Why use containers?
Containers keep code and tools together so your app works the same way on your laptop, on a server, or in Docker.

### How this project works

1. The browser opens the Flask website.
2. Flask reads project data from SQLite and renders HTML pages.
3. The home page fetches GitHub repos using the GitHub API.
4. The admin area adds, edits, and deletes projects in the database.
5. Docker can run the app in a container, and GitHub Actions checks the code automatically.

## Notes for Beginners

- The database file `database/portfolio.db` is created automatically when you first run the app.
- The admin login is simple and only for demo purposes.
- The demo is already configured to show repositories from `github.com/TejaReddyKuru`.
