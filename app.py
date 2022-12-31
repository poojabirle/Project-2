from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import processor


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///contact.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/chat', methods=["GET", "POST"])
def index():
    return render_template('chatbot.html', **locals())



@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_question = request.form['question']

        response = processor.chatbot_response(the_question)

    return jsonify({"response": response })
    

class Contact(db.Model):
    sno =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.email} - {self.subject} - {self.phone} - {self.message}"

@app.route("/")
def Home():
    return render_template('index.html')  

@app.route("/about")
def About():
    return render_template('about.html') 

@app.route("/team")
def Team():
    return render_template('team.html') 

@app.route("/service")
def Service():
    return render_template('service.html') 
 

@app.route("/contact", methods=['GET','POST'])
def Details():
    if  request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        phone = request.form['phone']
        message = request.form['message']
        contact = Contact(name = name, email=email,subject=subject,phone=phone,message=message)
        db.session.add(contact)
        db.session.commit()
    details = Contact.query.all()
    return render_template('contact.html') 
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
