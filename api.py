from nasabah import *
from face_recog import perhitungan_face_recognition

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
    today = datetime.now()
    data = request.get_json()
    get_nasabah = Nasabah.query.get(id)
    if data.get('isAuth'):
        get_nasabah.isAuth = data['isAuth']
    if data.get('auth_similarity'):
        get_nasabah.auth_similarity = data['auth_similarity']
    if data.get('foto_auth'):
        get_nasabah.foto_auth = data['foto_auth']
    get_nasabah.date_auth = today
    db.session.add(get_nasabah)
    db.session.commit()
    nasabah_schema = NasabahSchema(only=['id', 'id_nasabah', 'nama', 'phone', 'foto', 'foto_auth', 'alamat', 'isAuth', 'date_register', 'date_auth', 'auth_similarity'])
    nasabah = nasabah_schema.dump(get_nasabah)

    return make_response(jsonify({"nasabah": nasabah}))

# route untuk otentikasi by id
@app.route('/api/v1/otentikasi/<id>', methods = ['PUT'])
def otentikasi_by_id(id):
    # cek apakah img, id dan nama tersedia
    if request.files['img'] and request.form['id_nasabah']:
        # tangkap img dan id_nasabah dari form
        id_nasabah = str(request.form['id_nasabah'])
        foto = str(request.form['foto'])
        f = request.files['img']
        filename = secure_filename(f.filename)

        # cek direktori kalo belum ada
        # buat direktori folder sesuai nama
        if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah, 'auth')):
            if not os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah)):
                os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], id_nasabah), 0o777)
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], id_nasabah, 'auth'), 0o777)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah, 'auth', filename))

        # proses otentikasi 
        path_foto = os.path.join(app.config['UPLOAD_FOLDER'],id_nasabah, 'dataset', foto)
        array_auth = perhitungan_face_recognition(f, path_foto)


        return make_response(jsonify({"response": str(array_auth)}))
    return make_response(jsonify({"response": "file kosong!!"}))
    