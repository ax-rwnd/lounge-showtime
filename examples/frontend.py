from flask import Flask, render_template

app = Flask(__name__)

middle_url = "http://fiskpinnar.campus.ltu.se:5011/upload"
showtime_url = "http://fiskpinnar.campus.ltu.se:5012/ogg/elevatormusic.ogg"

@app.route('/upload-dialog', methods=['GET','POST'])
def dialog():
	""" Shows the upload dialog. """
	return render_template('upload.html', middle_url=middle_url)

@app.route('/lounge')
def lounge():
	return render_template('lounge.html', source=showtime_url)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5010, debug=True)
