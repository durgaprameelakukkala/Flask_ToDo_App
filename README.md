Welcome to SMRITI Web Project
A simple and elegant web app built with Flask that allows multiple users to manage their own task lists. Each user has their own account and can add, edit, complete, and delete tasks. Includes a visually enhanced UI with background/cover photos.



##  Features

- Secure user authentication (signup, login, logout)
- Add, complete, undo, delete, and edit tasks
- Each task is associated with a specific user
- Protected routes using `@login_required`
- Background/cover photo integration for a clean, modern look
- SQLite database for persistent storage

---

##  Installation

### 1. Clone the repository
```bash
git clone https://github.com/durgaprameelakukkala/Flask_ToDo_App.git
cd flask-task-manager
---

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

### 3. Install dependencies
```bash
pip install -r requirements.txt

### 4. Run the application
```bash
python app.py
Visit http://127.0.0.1:5000 in your browser.

### 5.Project Structure
flask-task-manager/
│
├── app.py                  # Main application file
├── tasks.db                # SQLite database (auto-created)
├── static/
│   └── images/             # Background and cover photos
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── edit.html
└── README.md

### 6.UI Notes
You can customize the UI with your own background/cover images. Place your images in the static/images/ directory and reference them in base.html, like so:
```bash
<style>
  body {
    background: url("{{ url_for('static', filename='images/bg.jpg') }}") no-repeat center center fixed;
    background-size: cover;
  }
</style>

### 7. requirements.txt
```bash
Flask==2.3.3
Flask-Login==0.6.3
Werkzeug==2.3.7
Flask==2.3.3
Flask-Login==0.6.3
Werkzeug==2.3.7

### 8.Authentication
Passwords are stored securely using werkzeug.security hashing
Flask-Login handles session management and user access control
Only logged-in users can access or modify their tasks
----
###License
This project is licensed under the MIT License.
----
## 🙋‍♀️ Author
**Durgaprameela Kukkala**  
[GitHub Profile](https://github.com/durgaprameelakukkala)

