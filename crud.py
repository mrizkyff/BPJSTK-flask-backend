from settings import *
import json
from nasabah import *


@app.route('/')
def index():
    all_nasabah = Nasabah.query.all()
    return render_template("index.html", nasabah = all_nasabah)

@app.route('/insert', methods= ['POST'])
def insert():
    today = datetime.now()
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
            id_nasabah = request.form['id_nasabah']
            # cek direktori kalo belum ada
            # buat direktori folder sesuai nama
            if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah, 'dataset')):
                if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah)):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], id_nasabah), 0o777)
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], id_nasabah, 'dataset'), 0o777)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'] ,id_nasabah, 'dataset' ,filename))
            # data untuk disimpan di database
            id_nasabah = request.form['id_nasabah']
            nama = request.form['nama']
            phone = request.form['phone']
            foto = filename
            foto_auth = "null"
            alamat = request.form['alamat']
            isAuth = "false"
            date_register = today
            date_auth = today
            auth_similarity = 0.0
            myNasabah = Nasabah(id_nasabah, nama, phone, foto, foto_auth, alamat, isAuth, date_register, date_auth, auth_similarity)
            db.session.add(myNasabah)
            db.session.commit()
            flash("Nasabah Berhasil Ditambahkan")
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