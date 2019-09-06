from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug import secure_filename
import os
import analyse
import utils
import zipfile

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
        print(request.form.to_dict())
        return render_template("index.html", type="upload", error="empty")


@app.route("/results", methods=["GET", "POST"])
def analysis_page():
    # Methods
    if not request.method == "POST":
        return redirect(url_for("main"))
    # Checking for files
    if request.files["file"].filename == "":
        return render_template("index.html", type="upload", error="Missing Excel file!")

    elif not request.files["file"].filename == "" and request.files["config"].filename == "":  # Build config
        excel = request.files["file"]
        excel_filename = secure_filename(excel.filename)
        directory = os.path.join(app.config["UPLOAD_FOLDER"], utils.secure(16))
        if not os.path.exists(directory):
            os.mkdir(directory)
            app.config["TEMP_FOLDER"] = directory
        excel.save(os.path.join(directory, excel_filename))

        questions = list(
            utils.parse_excel(os.path.join(directory, excel_filename)).keys()
        )
        prediction = utils.Predictor().predict(questions)
        questions_index = [
            [i + 1, question, prediction[i]] for i, question in enumerate(questions)
        ]

        return render_template(
            "index.html",
            type="config",
            questions=questions_index,
            error=None
        )

    else:
        # Saving files
        excel, config = request.files["file"], request.files["config"]
        excel_filename, config_filename = (
            secure_filename(excel.filename),
            secure_filename(config.filename),
        )
        directory = os.path.join(app.config["UPLOAD_FOLDER"], utils.secure(16))

        if not os.path.exists(directory):
            os.mkdir(directory)
        excel.save(os.path.join(directory, excel_filename))
        config.save(os.path.join(directory, config_filename))

        # TODO: Implement redirect to config_page with pre_filled in values
        # if len(
        #     utils.parse_excel(os.path.join(directory, excel_filename)).keys()
        # ) != len(utils.parse_config(os.path.join(directory, config_filename))):
        #     return "oh noes"

        # Work on file
        app.config["ANALYSIS"] = analyse.analyse(
            directory, excel_filename, config_filename
        )
        graphs, clouds, numerical = [], [], []
        for question, analysis in app.config["ANALYSIS"].items():
            if analysis:
                if analysis[0] == "categorical":
                    graphs.append(
                        [
                            question,
                            utils.pie(
                                question,
                                [x for x in analysis[1]["Percentages"].keys()],
                                [y for y in analysis[1]["Percentages"].values()],
                            ),
                        ]
                    )
                elif analysis[0] == "openended":
                    clouds.append([question, analysis[1]])
                elif analysis[0] == "numerical":
                    numerical.append([question, analysis[1]])
                else:
                    pass
        graphs = tuple(utils.chunk(graphs, 3))
        clouds = tuple(utils.chunk(clouds, 2))
        numerical = tuple(utils.chunk(numerical, 4))

        return render_template(
            "index.html",
            type="analyse",
            graphs=graphs,
            clouds=clouds,
            numerical=numerical,
            filename=excel_filename,
            path=os.path.split(directory)[1],
        )


@app.route("/download/<path>")
def download(path):
    doc = analyse.generate_report(
        os.path.join("./static/uploads/", path), app.config["ANALYSIS"]
    )
    file_names = [
        i[1] for i in app.config["ANALYSIS"].values() if i if i[0] == "openended"
    ]
    download_path = os.path.join("./static/uploads/", path, f"{utils.secure(4)}.zip")

    with zipfile.ZipFile(download_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for i in file_names:
            zipf.write(i, os.path.basename(i))
        zipf.write(doc, os.path.basename(doc))

    return send_file(
        download_path,
        mimetype="application/zip",
        attachment_filename="report.zip",
        as_attachment=True,
    )


app.run(port=80)
