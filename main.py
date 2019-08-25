from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
import analyse
import utils

app = Flask("app")
app.config["UPLOAD_FOLDER"] = "uploads"


def chunk(input, size):  # TODO: move to other file?
    for i in range(0, len(input), size):
        yield input[i : i + size]


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
    directory = os.path.join(app.config["UPLOAD_FOLDER"], excel_filename,"/files")
    cloud_dir = os.path.join(app.config["UPLOAD_FOLDER"], excel_filename,"/cloud")

    if not os.path.exists(directory):
        os.mkdir(directory)
        os.mkdir(cloud_dir)
    excel.save(os.path.join(directory, excel_filename))
    config.save(os.path.join(directory, config_filename))

    # Work on file
    results = analyse.analyse(directory, excel_filename, config_filename,cloud_dir)

    graphs = []
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
    graphs = tuple(chunk(graphs, 3))

    return render_template("index.html", graphs=graphs)


app.run(port=80)
