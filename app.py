from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import json
import google.generativeai as genai
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PIL import Image

app = Flask(__name__)

# Environment Variables
API_KEY = os.getenv("GENAI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GENAI_API_KEY")

# User Data
users = {'vrunda': '123', 'jayraj': '456'}
data = {'vrunda': [], 'jayraj': []}
active_user = ""

def configure_genai():
    """ Configures the Gemini AI model """
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-1.5-pro')

def extract_data_from_image(active_user, img):
    """ Extracts relevant data from an invoice image using GenAI """
    global data
    model = configure_genai()
    
    prompt = (
        "You need to fetch the data from this image. Respond in JSON format without triple quotes or json keyword.\n"
        "Keys required: [invoice_no, seller_name, cgst_amount, sgst_amount, bill_amount, date, expense_category (Personal, Entertainment, Medical, Household, Leisure, Education, Others); write NA if not available]"
    )
    
    response = model.generate_content([prompt, img])
    extracted_data = json.loads(response.text)
    data[active_user].append(extracted_data)
    return True

def generate_pdf(user_data):
    """ Generates a structured PDF report from extracted data """
    doc = SimpleDocTemplate("table.pdf", pagesize=letter)
    elements = []
    table_data = [list(i.values()) for i in user_data]

    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    return "table.pdf"

@app.route('/', methods=['GET', 'POST'])
def index():
    global active_user
    if active_user == '':
        return render_template('login.html')

    if request.method == 'POST':
        if 'img' in request.files:
            img_file = request.files.getlist('img')
            for img_data in img_file:
                img_bytes = img_data.read()
                img = Image.open(BytesIO(img_bytes))
                extract_data_from_image(active_user, img)
        else:    
            pdf_file = generate_pdf(data[active_user])
            return send_file(pdf_file, as_attachment=True, download_name='report.pdf')
            
    return render_template('index.html', data_display=data[active_user])

@app.route('/login', methods=['POST'])
def login():
    """ Handles user authentication """
    global active_user
    username = request.form['username']
    password = request.form['password']

    if users.get(username) == password:
        active_user = username
        return redirect(url_for('index'))
    
    return render_template('login.html', message='Invalid username or password')

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Using Render's PORT variable
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')
