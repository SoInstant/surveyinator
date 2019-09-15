import os
import zipfile

from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

import analyse
import utils

app = Flask("app")
app.config["UPLOAD_FOLDER"] = "./static/uploads/"
app.config["TEMP_FOLDER"] = None
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.mkdir(app.config["UPLOAD_FOLDER"])


def save_file(directory=None, excel_file=None, config_file=None):
    """Saves file(s) to directory

    Args:
        directory(str): Directory in which to save the files
        excel_file(class): An instance of the werkzeug.datastructures.FileStorage
            class containing the excel_file
        config_file(class): An instance of the werkzeug.datastructures.FileStorage
            class containing the config_file

    Returns:
        A dictionary containing the path to the directory the file(s) are saved in and
        the filename(s). For example:
        {
            "Directory": "./static/uploads/4SikvVjjqlWV44AW/",
            "Excel": "responses.xlsx",
            "Config": "config_file.txt"
        }
    """
    if not directory:
        directory = os.path.join(app.config["UPLOAD_FOLDER"], utils.secure(16))
    if not os.path.exists(directory):
        os.mkdir(directory)
    output = None
    if excel_file and config_file:
        excel_name = secure_filename(excel_file.filename)
        config_name = secure_filename(config_file.filename)
        excel_file.save(os.path.join(directory, excel_name))
        config_file.save(os.path.join(directory, config_name))
        output = {"Directory": directory, "Excel": excel_name, "Config": config_name}
    elif excel_file:
        excel_name = secure_filename(excel_file.filename)
        excel_file.save(os.path.join(directory, excel_name))
        output = {"Directory": directory, "Excel": excel_name, "Config": None}
    return output


@app.route("/", methods=["GET", "POST"])
def main():  # Homepage
    return render_template("index.html", type="upload", error=None)


@app.route("/config", methods=["GET", "POST"])
def config_page():
    if not request.method == "POST":
        return redirect(url_for("main"))
    else:
        config = utils.to_config(directory=app.config["TEMP_FOLDER"], config=request.form.to_dict())
        for file in os.listdir(app.config["TEMP_FOLDER"]):
            if file.endswith(".xlsx"):
                excel = os.path.join(app.config["TEMP_FOLDER"], file)
        return redirect(url_for("analysis_page", excel=excel, config=config))


@app.route("/results", methods=["GET", "POST"])
def analysis_page():
    # Methods
    excel, config = request.args.get("excel"), request.args.get("config")
    if (not request.method == "POST") and (not excel and not config):
        return redirect(url_for("main"))
    # Checking for files
    do_analysis = False
    if request.method == "GET":
        if excel and config:
            do_analysis = True
    elif request.method == "POST" and (request.files["file"] and request.files["config"]):
        do_analysis = True

    # Do analysis
    if do_analysis:
        # Saving files
        if request.method == "POST":
            save = save_file(excel_file=request.files["file"], config_file=request.files["config"])
            directory, excel_filename, config_filename = save["Directory"], save["Excel"], save["Config"]
        else:
            directory, excel_filename = os.path.split(excel)
            config_filename = os.path.basename(config)

        questions = list(utils.parse_excel(os.path.join(directory, excel_filename)).keys())
        types = utils.parse_config(os.path.join(directory, config_filename))

        # Excel but incomplete config
        if len(questions) != len(types):
            app.config["TEMP_FOLDER"] = directory
            predictor = utils.Predictor()
            qn_dict = {}
            for i, qn in enumerate(questions):
                if i + 1 not in types.keys():
                    datatype = predictor.predict([qn])
                    qn_dict[i + 1] = (qn, datatype[0])
                else:
                    qn_dict[i + 1] = (qn, types[i + 1])
            questions_index = [(i[0], i[1][0], i[1][1]) for i in qn_dict.items()]

            return render_template(
                "index.html", type="config", questions=questions_index, error=None
            )

        # Start analysis
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

        graphs = tuple(utils.chunk(graphs, 3))
        clouds = tuple(utils.chunk(clouds, 2))
        numerical = tuple(utils.chunk(numerical, 4))

        return render_template(
            "index.html",
            type="analysis",
            graphs=graphs,
            clouds=clouds,
            numerical=numerical,
            filename=excel_filename,
            path=os.path.split(directory)[1],
        )
    elif not request.files["file"]:  # No excel
        return render_template("index.html", type="upload", error="Missing Excel file!")

    elif request.files["file"] and not request.files["config"]:  # Excel but no config
        save = save_file(excel_file=request.files["file"])
        directory, excel_filename = save["Directory"], save["Excel"]
        app.config["TEMP_FOLDER"] = directory
        questions = list(utils.parse_excel(os.path.join(directory, excel_filename)).keys())
        predictions = utils.Predictor().predict(questions)
        questions_index = [
            (i + 1, question, predictions[i]) for i, question in enumerate(questions)
        ]

        return render_template(
            "index.html", type="config", questions=questions_index, error=None
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


# Error handling
error_messages = {404: "Page not Found", 403: "Forbidden", 410: "Gone", 500: "Internal Server Error"}


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def page_error(error):
    error_no = int(str(error)[:3])
    error_message = error_messages[error_no]
    return render_template("index.html", type="error", error_no=error_no, error_message=error_message)


app.run(port=80)
