from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)


@app.route("/")
@app.route("/<path:subpath>")
def index(subpath=None):
    if subpath == "favicon.ico":
        return send_file(path_or_file=f"./icon.png", mimetype="image")

    substring = subpath if subpath is not None else ''

    if subpath is not None:
        if ".mp3" in subpath:
            return send_file(path_or_file=f"./content/{subpath}", mimetype="audio/mpeg")

    directory_list = os.listdir(f"./content/{substring}")
    for i, e in enumerate(directory_list):
        if "." not in e:
            directory_list.insert(0, directory_list.pop(i)) # put all directories first
    innerhtml = "<table>"
    innerhtml += f"<tr><th><a href='/{''.join(substring.split('/')[:-1])}'>↑back↑</a></th></tr>" if subpath else ""
    for i in directory_list:
        if "." not in i:
            innerhtml += f"<tr><th><a href='{'/' + substring if subpath else ''}/{i}'>{i}</a></th></tr>"
        elif ".mp3" in i:
            innerhtml += f"<tr><th>{i}</th><td><audio controls src='{'/' + substring if subpath else ''}/{i}'</td></tr>"
    innerhtml += "</table>"

    title = "index"
    if subpath:
        title = substring.split("/")[-1]

    return render_template("index.html", body=innerhtml, title=title)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)