from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

UPLOAD_FOLDER = 'static/images/dataset'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.secret_key = 'SECRET KEY'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/employees'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    foto = db.Column(db.String(255))

    
    def __init__(self, name, email, phone, foto):
        self.name = name
        self.email = email
        self.phone = phone
        self.foto = foto
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)

@app.route('/insert', methods= ['POST'])
def insert():
    if request.method == 'POST':
        if 'foto' not in request.files:
            flash('No File Part')
            return redirect(request.url)
        file = request.files['foto']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # buat direktori folder sesuai nama
            os.mkdir(os.path.join('static/images/dataset',request.form['name']))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] ,request.form['name'] ,filename))
            # data untuk disimpan di database
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            foto = filename
            mydata = Data(name, email, phone, foto)
            db.session.add(mydata)
            db.session.commit()
            flash("Employee Inserted Successfully")
            return redirect(url_for('index'))


@app.route('/update', methods= ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully!")

        return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash('Employee Deleted Successfully!')

    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['foto']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return file.filename

if __name__ == "__main__":
    app.run(debug=True)