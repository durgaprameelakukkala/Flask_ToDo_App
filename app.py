from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key!
DATABASE = 'tasks.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect unauthorized users to login page

class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
    if user:
        return User(*user)
    return None

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

@app.route('/')
@login_required
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, completed FROM tasks WHERE user_id = ?", (current_user.id,))
        tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
@login_required
def add():
    task_content = request.form['content'].strip()
    if not task_content:
        flash('Task content cannot be empty.', 'warning')
        return redirect(url_for('index'))
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("INSERT INTO tasks (content, completed, user_id) VALUES (?, ?, ?)",
                     (task_content, False, current_user.id))
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?", (task_id, current_user.id))
    flash('Task marked as complete.', 'info')
    return redirect(url_for('index'))

@app.route('/undo/<int:task_id>', methods=['POST'])
@login_required
def undo(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("UPDATE tasks SET completed = 0 WHERE id = ? AND user_id = ?", (task_id, current_user.id))
    flash('Task marked as incomplete.', 'info')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, current_user.id))
    flash('Task deleted.', 'danger')
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    if request.method == 'POST':
        new_content = request.form.get('content', '').strip()
        if not new_content:
            flash("Content cannot be empty.", "danger")
            return redirect(url_for('edit', task_id=task_id))
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "UPDATE tasks SET content = ? WHERE id = ? AND user_id = ?",
                (new_content, task_id, current_user.id)
            )
        flash('Task updated successfully.', 'success')
        return redirect(url_for('index'))

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT content FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, current_user.id)
        )
        task = cursor.fetchone()
    if not task:
        flash("Task not found or unauthorized.", "danger")
        return redirect(url_for('index'))
    content = task[0]
    return render_template('edit.html', content=content, task_id=task_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Please fill in both username and password.', 'warning')
            return redirect(url_for('signup'))
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                flash('Username already exists. Choose a different one.', 'danger')
                return redirect(url_for('signup'))
            password_hash = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            user_obj = User(*user)
            login_user(user_obj)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username or password.', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
