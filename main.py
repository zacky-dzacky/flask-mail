import os
from flask import Flask, render_template
from flask_mail import Mail, Message
from threading import Thread

app = Flask(__name__)
mail = Mail()

# configuration of mail 
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['TESTING'] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL') # Ganti dengan email
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD') # Ganti dengan password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEBUG'] = True
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)


def shell_context():
    import os, sys
    return dict(app=app, os=os, sys=sys)

def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)
        print("Email terkirim")


def send_email(message):

    # os.environ.get('RECIPIENT') diubah menjadi email penerima
    msg = Message("Title", sender="sender@gmail.com", recipients=[os.environ.get('RECIPIENT')],body=message)
    msg.html = render_template('mail.html')
    
    # mail.send(msg) //diaktifkan jika tidak menggunakan threading

    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()

@app.route("/")
def index():
    send_email("Hello")
    return "Success"

if __name__ == "__main__":
    app.run(port=8000, debug=True)