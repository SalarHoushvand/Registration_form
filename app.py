import os
from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect, secure_filename

# define allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# set upload directory
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/static/images/user_img'

# set app configs and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rqodnvybmqdysn:9ee3977d1c8650443397c39fab330bb7daba062a4acb34783c9194319a4fdc04@ec2-52-22-216-69.compute-1.amazonaws.com:5432/d2pj7anncnudvr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.debug = True
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# check allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# class for creating tables for postgres database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    number = db.Column(db.String(15), unique=False)
    street = db.Column(db.String(120), unique=False)
    city = db.Column(db.String(120), unique=False)
    state = db.Column(db.String(120), unique=False)
    zip = db.Column(db.Integer, unique=False)
    feedback = db.Column(db.String(300), unique=False)
    img_link = db.Column(db.String(500), unique=False)

    def __init__(self, username, email, number, street, city, state, zip, feedback, img_link):
        self.username = username
        self.email = email
        self.number = number
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.feedback = feedback
        self.img_link = img_link

    def __repr__(self):
        return '<User %r>' % self.username


# creating all the columns in table
db.create_all()

# main function to upload form data to database
@app.route("/", methods=['GET', 'POST'])
def form():

    global img_link
    if request.method == 'POST':

        # getting image and adding to the folder
        # check if the post request has the file part
        if 'file' not in request.files:
            log = 'Image field is empty.'
            return render_template('fail.html', log = log)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            log = 'Empty filename.'
            return render_template('fail.html', log=log)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_link = '../static/images/user_img/' + filename

        # text data for postgres
        user = User(request.form['username'],
                    request.form['email'],
                    request.form['number'],
                    request.form['street'],
                    request.form['city'],
                    request.form['state'],
                    request.form['zip'],
                    request.form['feedback'],
                    img_link
                    )
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('success'))
    else:
        return render_template('home.html')


# function for rendering the success.html after submitting the form
@app.route("/success")
def success():
    my_user = User.query.all()
    return render_template('success2.html', my_user=my_user[-1])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
