import os
from werkzeug import secure_filename
from flask import Flask, Response, request
from config import Config
from seated import send_post

app =Flask(__name__)
cfg = Config()

@app.route("/ogg")
def streamogg():
	def generate():
		with open("signals/elevatormusic.ogg", "rb") as fogg:
			data = fogg.read(1024)
			while data:
				yield data
				data = fogg.read(1024)
	return Response(generate(), mimetype="audio/ogg")

@app.route('/upload', methods=['POST'])
def uploadfile():
	""" Accept file from outside source. """

	print "files:",request.files
	for key in  request.files.iterkeys():
		stream = request.files[key]

		path = os.path.join("signals/",key)
		with open(path, "wb") as ofile:
			while ofile:
				ofile.write(stream.read(1024))
		

	return "Done"

if __name__ == "__main__":
	app.run(host=cfg.host, port=cfg.port, debug=True)

