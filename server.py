from flask import Flask
from flask import request
from flask import render_template
import json
import os
# sudo python -m pip install flask-cors
from flask_cors import CORS
from os import walk

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    files = []
    for (dirpath, dirnames, filenames) in walk("jobs"):
        for file in filenames:
            files.append(file.replace(".py", ""))
    return render_template("index.html", files=files)

@app.route("/<name>")
def job(name):
    data = ""
    try:
        data = request.args.to_dict()
        cmd = "python jobs/{}.py '{}'".format(name, json.dumps(data))
        stream = os.popen(cmd)
        result = stream.read()
        if result == "":
            return "Empty output. Possible error on job {}".format(name)
        return result
    except:
        return "Error on job {}".format(name)


app.run(port=80)
