from settings import *
import json

# inisialisasi database
db = SQLAlchemy(app)


# class Nasabah inherit dari db.Model dari SQLAlchemy
class Nasabah(db.Model):
    __tablename__ = "nasabah"
    id = db.Column(db.Integer, primary_key=True)
    id_nasabah = db.Column(db.String(16), nullable=False)
    nama = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    foto = db.Column(db.String(255), nullable=False)
    alamat = db.Column(db.Text(), nullable=False)
    isAuth = db.Column(db.Boolean, server_default="false", default=False)
    date_register = db.Column(db.DateTime(), nullable=True, default=datetime.now())
    date_auth = db.Column(db.DateTime(), nullable=True, default=datetime.now())
    auth_similarity = db.Column(db.Float(), nullable=True, default=0.0)

    def __init__(self, id_nasabah, nama, phone, foto, alamat, isAuth, date_register, date_auth, auth_similarity):
        self.id_nasabah = id_nasabah
        self.nama = nama
        self.phone = phone
        self.foto = foto
        self.alamat = alamat
        self.isAuth = isAuth
        self.date_register = date_register
        self.date_auth = date_auth
        self.auth_similarity = auth_similarity
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return F"{self.id}"

db.create_all()


# serializer untuk nasabah
class NasabahSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Nasabah
        sqla_session = db.session
    id = fields.Integer(dump_only=True)
    id_nasabah = fields.String(required=True)
    nama = fields.String(required=True)
    phone = fields.String(required=True)
    foto = fields.String(required=True)
    alamat = fields.String(required=True)
    isAuth = fields.Boolean(required=False)
    date_register = fields.DateTime(required=False)
    date_auth = fields.DateTime(required=False)
    auth_similarity = fields.Float(required=False)

