from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
import analyse
import utils

app = Flask("app")
app.config["UPLOAD_FOLDER"] = "static/uploads"


@app.route("/", methods=["GET", "POST"])
def main():  # Homepage
    return render_template("upload.html", error="")


@app.route("/results", methods=["GET", "POST"])
def analysis_page():
    # Methods
    if not request.method == "POST":
        return redirect(url_for("main"))

    # Checking for files
    if not request.files["file"]:
        return render_template("upload.html", error="Missing excel file!")
    if not request.files["config"]:  # Remove when config setup website done
        return render_template("upload.html", error="Missing config file!")

    # Saving files
    excel = request.files["file"]
    excel_filename = secure_filename(excel.filename)
    config = request.files["config"]
    config_filename = secure_filename(config.filename)
    directory = os.path.join(app.config["UPLOAD_FOLDER"], excel_filename)

    if not os.path.exists(directory):
        os.mkdir(directory)
    excel.save(os.path.join(directory, excel_filename))
    config.save(os.path.join(directory, config_filename))

    # Work on file
    results = analyse.analyse(directory, excel_filename, config_filename)

    graphs = []
    clouds = []
    for question, analysis in results.items():
        if analysis:
            if analysis[0] == "categorical":
                graphs.append(
                    utils.pie(
                        question,
                        [x for x, y in analysis[1]["Percentages"].items()],
                        [y for x, y in analysis[1]["Percentages"].items()],
                    )
                )
            elif analysis[0] == "openended":
                clouds.append(analysis[1])
    graphs = tuple(utils.chunk(graphs, 2))
    clouds = tuple(utils.chunk(clouds, 2))

    return render_template("index.html", graphs=graphs, clouds=clouds)


app.run(port=80)
