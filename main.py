from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug import secure_filename
import os
import analyse
import utils

app = Flask("app")
app.config["UPLOAD_FOLDER"] = "./static/uploads/"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.mkdir(app.config["UPLOAD_FOLDER"])


@app.route("/", methods=["GET", "POST"])
def main():  # Homepage
    return render_template("index.html", type="upload", error=None)


@app.route("/config", methods=["GET", "POST"])
def config_page():
    if not request.method == "POST":
        return redirect(url_for("main"))
    else:
        print(request.form)
        return render_template("index.html", type="upload", error=None)


@app.route("/results", methods=["GET", "POST"])
def analysis_page():
    # Methods
    if not request.method == "POST":
        return redirect(url_for("main"))
    # Checking for files
    if not request.files["file"]:
        return render_template("index.html", type="upload", error="Missing Excel file!")

    elif request.files["file"] and not request.files["config"]:  # Build config
        excel = request.files["file"]
        excel_filename = secure_filename(excel.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"], utils.secure(16))
        if not os.path.exists(directory):
            os.mkdir(directory)
        excel.save(os.path.join(directory, excel_filename))

        questions = list(
            utils.parse_excel(os.path.join(directory, excel_filename)).keys()
        )
        questions_index = []
        prediction = utils.Predictor().predict(questions)
        for index, question in enumerate(questions):
            questions_index.append([index + 1, question, prediction[index]])
        return render_template(
            "index.html", type="config", questions=questions_index, error=None
        )
    else:
        # Saving files
        excel = request.files["file"]
        excel_filename = secure_filename(excel.filename)
        config = request.files["config"]
        config_filename = secure_filename(config.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"], utils.secure(16))

        if not os.path.exists(directory):
            os.mkdir(directory)
        excel.save(os.path.join(directory, excel_filename))
        config.save(os.path.join(directory, config_filename))

        # Work on file
        results = analyse.analyse(directory, excel_filename, config_filename)
        app.config["ANALYSIS"] = results
        graphs = []
        clouds = []
        for question, analysis in results.items():
            if analysis:
                if analysis[0] == "categorical":
                    graphs.append(
                        [
                            question,
                            utils.pie(
                                question,
                                [x for x, y in analysis[1]["Percentages"].items()],
                                [y for x, y in analysis[1]["Percentages"].items()],
                            ),
                        ]
                    )
                elif analysis[0] == "openended":
                    clouds.append([question, analysis[1]])
        graphs = tuple(utils.chunk(graphs, 3))
        clouds = tuple(utils.chunk(clouds, 2))

        return render_template(
            "index.html",
            type="analyse",
            graphs=graphs,
            clouds=clouds,
            filename=excel_filename,
            path=os.path.split(directory)[1],
        )


@app.route("/download/<path>")
def download(path):
    download_path = analyse.generate_report(
        os.path.join("./static/uploads/", path), app.config["ANALYSIS"]
    )
    return send_file(
        download_path,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        attachment_filename="report.docx",
        as_attachment=True,
    )


app.run(port=80)
