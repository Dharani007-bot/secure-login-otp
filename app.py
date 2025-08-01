from flask import Flask, render_template, request, redirect, session, flash
import sqlite3, smtplib, random
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Connection
def get_db():
    conn = sqlite3.connect('database.db')
    return conn

# OTP Generator
def generate_otp():
    return str(random.randint(100000, 999999))

# Email Sender
def send_otp_email(receiver_email, otp):
    sender = 'dharaniml2005@gmail.com'  # ✅ Replace with your Gmail
    password = 'duve ldkv snio eflk'  # ✅ Replace with Gmail App Password

    msg = MIMEText(f'Your OTP is {otp}')
    msg['Subject'] = 'Login OTP'
    msg['From'] = sender
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ OTP sent to {receiver_email}: {otp}")  # Debug
    except Exception as e:
        print("❌ Failed to send email:", e)

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            otp = generate_otp()
            session['email'] = email
            session['otp'] = otp
            send_otp_email(email, otp)
            return redirect('/verify')
        else:
            flash('❌ Invalid credentials')
    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            return redirect('/dashboard')
        else:
            flash('❌ Incorrect OTP')
    return render_template('otp_verify.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        flash('✅ Registration successful. Please login.')
        return redirect('/')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
