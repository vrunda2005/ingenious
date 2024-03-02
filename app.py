# Your Flask application code

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
users = {
    'vrunda' : '123',
    'jayraj' : "456" 
}

@app.route("/")
def main():
    return render_template("index.html")


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        # Successful login, redirect to a dashboard or profile page
        return redirect(url_for('index'))
    else:
        # Login failed, redirect back to the login page with a message
        return render_template('login.html', message='Invalid username or password')


@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
