from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import face_recognition
from flask_cors import CORS

def perhitungan_face_recognition(file_stream, known_stream):
	face_found = False
	identified = False
	diff = 1.0

	# image yang dikenali
	known_image = face_recognition.load_image_file(known_stream)
	known_image_encoding = face_recognition.face_encodings(known_image)[0]

	# image yang akan diuji
	unknown_image = face_recognition.load_image_file(file_stream)
	unknown_image_encoding = face_recognition.face_encodings(unknown_image)[0]

	if len(unknown_image_encoding) > 0:
		face_found = True
		# cek kecocokan
		match_result = face_recognition.compare_faces([known_image_encoding], unknown_image_encoding)
		# hitung jarak / perbedaan
		diff = diff-(face_recognition.face_distance([known_image_encoding], unknown_image_encoding))

		if match_result[0]:
			identified = True

	# return as json
	result = {
		"face_found_in_image": face_found,
		"is_identified": identified,
		"similarity": float(diff)
	}
	return result