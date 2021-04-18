from nasabah import *

# route untuk get all nasabah
@app.route('/api/v1/nasabah', methods=['GET'])
def get_all_nasabah():
    get_nasabah = Nasabah.query.all()
    nasabah_schema = NasabahSchema(many=True)
    nasabah = nasabah_schema.dump(get_nasabah)
    return make_response(jsonify({"nasabah": nasabah}))

# route untuk post nasabah
@app.route('/api/v1/nasabah', methods = ['POST'])
def create_nasabah():
    data = request.get_json()
    nasabah_schema = NasabahSchema()
    nasabah = nasabah_schema.load(data)
    result = nasabah_schema.dump(nasabah.create())
    return make_response(jsonify({"nasabah": result}), 200)

# route untuk get nasabah by id
@app.route('/api/v1/nasabah/<id>', methods = ['GET'])
def get_nasabah_by_id(id):
    get_nasabah = Nasabah.query.get(id)
    nasabah_schema = NasabahSchema()
    nasabah = nasabah_schema.dump(get_nasabah)
    return make_response(jsonify({"nasabah": nasabah}))

# route untuk update nasabah by id
@app.route('/api/v1/nasabah/<id>', methods = ['PUT'])
def update_nasabah_by_id(id):
    data = request.get_json()
    get_nasabah = Nasabah.query.get(id)
    if data.get('isAuth'):
        get_nasabah.isAuth = data['isAuth']
    db.session.add(get_nasabah)
    db.session.commit()
    nasabah_schema = NasabahSchema(only=['id', 'id_nasabah', 'nama', 'phone', 'foto', 'alamat', 'isAuth', 'date_register', 'date_auth'])
    nasabah = nasabah_schema.dump(get_nasabah)

    return make_response(jsonify({"nasabah": nasabah}))

# route untuk otentikasi by id
@app.route('/api/v1/otentikasi/<id>', methods = ['PUT'])
def otentikasi_by_id(id):
    # cek apakah img, id dan nama tersedia
    if request.files['img'] and request.form['id_nasabah']:
        # tangkap img dan id_nasabah dari form
        id_nasabah = request.form['id_nasabah']
        f = request.files['img']
        filename = secure_filename(f.filename)

        # cek direktori kalo belum ada
        # buat direktori folder sesuai nama
        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], 'auth',id_nasabah)):
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], 'auth',id_nasabah), 0o777)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'auth',id_nasabah, filename))
        return make_response(jsonify({"response": "file berhasil disimpan di folder"+id_nasabah}))
    return make_response(jsonify({"response": "file kosong!!"}))
    