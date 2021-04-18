from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

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
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f"{self.id}"

db.create_all()

class DataSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Data
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)
    foto = fields.String(required=True)
    
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
            # cek direktori kalo belum ada
            # buat direktori folder sesuai nama
            if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],request.form['name'])):
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],request.form['name']), 0o777)

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

@app.route('/api/v1/data', methods = ['POST'])
def create_data():
    data = request.get_json()
    data_schema = DataSchema()
    datas = data_schema.load(data)
    result = data_schema.dump(datas.create())
    return make_response(jsonify({"todo": result}), 200)
    
@app.route('/api/v1/data', methods = ['GET'])
def index1():
    get_data = Data.query.all()
    data_schema = DataSchema(many=True)
    data = data_schema.dump(get_data)
    return make_response(jsonify({"data": data}))

@app.route('/api/v1/data/<id>', methods = ['GET'])
def get_data_by_id(id):
    get_data = Data.query.get(id)
    data_schema = DataSchema()
    data = data_schema.dump(get_data)
    return make_response(jsonify({"data": data}))
    
@app.route('/api/v1/data/<id>', methods = ['PUT'])
def update_data_by_id(id):
    data = request.get_json()
    get_data = Data.query.get(id)
    if data.get('name'):
        get_data.name = data['name']
    db.session.add(get_data)
    db.session.commit()
    data_schema = DataSchema(only=['id', 'name', 'email', 'phone', 'foto'])
    data = data_schema.dump(get_data)

    return make_response(jsonify({"data": data}))


if __name__ == "__main__":
    app.run(debug=True)