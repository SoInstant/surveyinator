from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
import analyse

app = Flask('app')
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def main(): #Homepage
  return render_template("upload.html", error="")

@app.route("/results", methods=["GET", "POST"])
def analysis_page():
    if request.method == "POST":
        if not request.files:
            return render_template("upload.html", error="Missing file!")
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return redirect(url_for('main'))
    return "no"

app.run()
