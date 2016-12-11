import os
from flask import Flask, Request, request
from werkzeug import secure_filename
import requests

app = Flask(__name__)

showtime_url = "http://fiskpinnar.campus.ltu.se:5012/upload"
upload_folder = 'tmp/'


app.route("/upload-complete", methods=["POST"])
def handle_upload_response():
	"""This will be called after every upload, but we can ignore it"""
	print "Uploaded!"
	return "Success"

@app.route("/upload", methods=["POST"])
def upload():
	flist = request.files
	for f in request.files.getlist("file[]"):
		path = os.path.join(upload_folder,secure_filename(f.filename))
		f.save(path)
		datas = {'username':'rwnd', 'session':'aaaaaaaaaaaa'}
		r = requests.post(showtime_url, files={'username':'relaxz', 'session':'$2b$12$djgtiCRDyAbm/a1zvLcjiuhurK.bWsdNs.xYq2dj.Nm0cKTuj0uiu',f.filename: open(path, 'rb')})
	
	
	#headers = {'Content-Type': 'application/json'}
	#print requests.post(showtime_url, files=flist,headers=headers)
	#for f in request.files.getlist("file[]"):
	#	data = {'file':(f.filename,f.stream,f.content_type, f.headers)}
	#	response = requests.post(showtime_url, data, "multipart/form-data")
	#	print response
	return "Done"

	#fp = request.files["name_of_file"]
	#url = create_upload_url(url_for('handle_upload_response'))
	#response = requests.post(url, {'file':
	#		(fp.filename, fp.stream,
	#		fp.content_type, fp.headers)})
	#if response == "Success":
	#	return "File uploaded successfully"
	#else:
	#	return "Something didn't work out"

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5011, debug=True)
