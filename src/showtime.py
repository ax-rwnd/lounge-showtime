import os, magic
from werkzeug import secure_filename
from flask import Flask, Response, request
from config import Config
from seated import send_post

app =Flask(__name__)
cfg = Config()

@app.route("/ogg/<string:song>")
def streamogg(song):
	def generate():
		path = os.path.join(cfg.data_path,song)
		with open(path, "rb") as fogg:
			data = fogg.read(1024)
			while data:
				yield data
				data = fogg.read(1024)

	return Response(generate(), mimetype="audio/ogg")

@app.route('/upload', methods=['POST'])
def uploadfile():
	""" Accept file from outside source. """

	# grab auth info
	user = request.files['username'].stream.read(32)
	session = request.files['session'].stream.read(60)

	status = send_post(cfg, '/api/auth', {'username':user,'session':session})
	if status['status'] == u'AUTH_OK':
		for key in  request.files.iterkeys():
			if key == 'username' or key == 'session':
				pass
			else:
				stream = request.files[key]
				
				# make sure that directory exists
				targetdir = os.path.join(cfg.data_path,user)
				try:
					os.makedirs(targetdir)
				except os.error:
					print "warning, oserror"
				
				path = os.path.join(targetdir,key)
				print "path:",path
				with open(path, "wb") as ofile:
					data = stream.read(1024)
					while len(data)>0:
						ofile.write(data)
						data = stream.read(1024)

				# remove files that turn out to be non-ogg
				if "audio/ogg" != magic.from_file(path, mime=True):
					os.remove(path)
				else:
					send_post(cfg, '/api/music', {'username':user, 'action':'ADD', 'path':path, 'title':key})
		return 'UPLOAD_OK'
	else:
		return 'UPLOAD_FAIL'


if __name__ == "__main__":
	app.run(host=cfg.host, port=cfg.port, debug=True)

