from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
app = Flask('app')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def main(): #Homepage
  return render_template("upload.html", error="")

@app.route("/results", methods=["GET, POST"])
def analysis_page():
    if request.method == "POST":
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    else:
        return redirect(url_for('main'))
    return "no"
    #request.form
    #return render_template("index.html")
app.run()
