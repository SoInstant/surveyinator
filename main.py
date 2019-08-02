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
    #Methods
    if not request.method == "POST":
        return redirect(url_for('main'))

    #Checking for files
    if not len(request.files) == 2:
        return render_template("upload.html", error="Missing files!")
    if not request.files["file"]:
        return render_template("upload.html", error="Missing excel file!")
    if not request.files["config"]: #Remove when config setup website done
        return render_template("upload.html", error="Missing config file!")

    #Saving files
    excel = request.files['file']
    excel_filename = secure_filename(excel.filename)
    config = request.files['config']
    config_filename = secure_filename(config.filename)
    directory = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

    if not os.path.exists(directory):
        os.mkdir(directory)
    excel.save(os.path.join(directory, excel_filename))
    config.save(os.path.join(directory, config_filename))

    #Work on file
    analyse.analyse(
        os.path.join(directory, excel_filename),
        os.path.join(directory, config_filename)
    )
    
    return render_template("index.html")
=

app.run(port=80)
