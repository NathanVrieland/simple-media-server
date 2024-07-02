from flask import Flask, render_template, request, send_file, redirect, make_response
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from io import BytesIO
import os
import hashlib
import mysecrets

app = Flask(__name__)

@app.route("/authenticate")
def auth():
    if request.args.get("password"):
        if hashlib.sha256(request.args.get("password").encode('utf-8')).digest() in mysecrets.passwords:
            resp = make_response(redirect('/'))
            resp.set_cookie("auth", mysecrets.cookie)
            return resp
        else:
            print(hashlib.sha256(request.args.get("password").encode('utf-8')).digest())
            return redirect("/authenticate")
    else:
        innerhtml = "<form method='GET' action='/authenticate'><label for='password'>password: </label><input type='password' name='password' id='password'></input></form>"
        return render_template("index.html", body=innerhtml, title="login")

@app.route("/")
@app.route("/<path:subpath>")
def index(subpath=None):
    if request.cookies.get("auth") == mysecrets.cookie:
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
        innerhtml = "<table class='table'>"
        innerhtml += f"<tr class=''><th><a href='/{''.join(substring.split('/')[:-1])}' class='btn btn-primary'>↑back↑</a></th><th style='padding: 0px; width: 50%;' colspan='2'><span id='currentsong'></span></th></tr>" if subpath else ""
        for i in directory_list:
            if "." not in i:
                innerhtml += f"<tr><th colspan='2'><a href='{'/' + substring if subpath else ''}/{i}' class='btn btn-success'>{i}</a></th></tr>"
            elif ".mp3" in i:
                innerhtml += f"<tr class=''><td><img src='{'icons/' + substring if subpath else ''}/{i}'/></td><th>{i.replace('.mp3', '')}</th><td class='d-flex justify-content-start'><audio controls preload='none' src='{'/' + substring if subpath else ''}/{i}'</td></tr>"
        innerhtml += "</table>"

        fileuploadform = f"""
        <div>
            <form method='post' action='/upload' class='form-group d-flex' enctype='multipart/form-data'>
                <input type="file" name="fileupload" id="fileupload" class='form-control-file' style='width: fit-content;'>
                <input type="hidden" name="path" value="{substring}">
                <input type="submit" value="upload" class='btn btn-primary'>
            </form>
        </div>
        """

        if substring:
            innerhtml += fileuploadform

        title = "index"
        if subpath:
            title = substring.split("/")[-1]

        return render_template("index.html", body=innerhtml, title=title)
    else:
        return redirect("/authenticate")

@app.route("/icons/<path:subpath>")
def icons(subpath):
    audio = MP3(f"./content/{subpath}", ID3=ID3)
    mp3buffer = BytesIO()
    for tag in audio.tags.values():
        if isinstance(tag, APIC):
            mp3buffer.write(tag.data)
            mp3buffer.seek(0)
            return send_file(mp3buffer, mimetype="image")
    return send_file("./default/cover.png", mimetype="image")

@app.route("/upload", methods=["POST"])
def upload():
    if request.cookies.get("auth") == mysecrets.cookie:
        if request.method == "POST":
            file = request.files["fileupload"]
            path = request.form["path"]
            file.save(f"./content/{path}/{file.filename}")
            return redirect(f"/{path}")
    else:
        return redirect("/authenticate")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)