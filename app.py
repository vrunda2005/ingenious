from flask import Flask, render_template, request, redirect, url_for
import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image
import json
app = Flask(__name__)
users = {
    'vrunda': '123',
    'jayraj': '456' 
}
data = {'vrunda': [],
        'jayraj': []}


activeUser = ""

def dataMaker(activeUser, img):
    global data
    print('datamaker',activeUser)
    genai.configure(api_key='AIzaSyBLb-imm7q-1VwWYo6Ia03ap13py0L5mSU')
    model = genai.GenerativeModel('gemini-pro-vision')
    
    response = model.generate_content(["You need to fetch the data from this image. Respond back in JSON string format without triple quotes and json keyword. These should be the keys of the data in JSON [invoice_no, name of seller, cgst_amount, sgst_amount, bill_amount, date, category of expense from:(Personal, Entertainment, Medical, Household, Leisure, Education, Others); write NA for data not available]", img])
    d = json.loads(response.text)
    data[activeUser].append(d)
    print(response.text)
    return True

def dataDisplay(activeUser):
    global data
    if data[activeUser]:
        # temp = f"<tr><td> {data[activeUser][0]['invoice_no']} </td><td>Francisco Chang</td><td>Mexico</td></tr>"
        return data[activeUser]
    else:
        return "help"

@app.route('/', methods=['GET', 'POST'])
def index():
    global activeUser
    if activeUser == '':
        return render_template('login.html')
    if request.method == 'POST':
        print('post',activeUser)
        if 'img' in request.files:
            img_file = request.files['img']
            img_bytes = img_file.read()
            img = Image.open(BytesIO(img_bytes))
            dataMaker(activeUser, img)
    data_display = dataDisplay(activeUser)  # Assign result to a different variable
    return render_template('index.html',data_display=data_display)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    global activeUser
    if username in users and users[username] == password:
        activeUser = username
        return redirect(url_for('index'))
    else:
        return render_template('login.html', message='Invalid username or password')

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)