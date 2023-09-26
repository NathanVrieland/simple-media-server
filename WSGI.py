from flask import Flask, render_template, request, send_file, redirect, make_response
import os
import secrets

app = Flask(__name__)

@app.route("/authenticate")
def auth():
    if request.args.get("password") in secrets.passwords:
        resp = make_response(redirect('/'))
        resp.set_cookie("auth", secrets.cookie)
        return resp
    else:
        innerhtml = "<form method='GET' action='/authenticate'><input type='password' name='password' id='password'></input></form>"
        return render_template("index.html", body=innerhtml, title="login")

@app.route("/")
@app.route("/<path:subpath>")
def index(subpath=None):
    if request.cookies.get("auth") == secrets.cookie:
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
        innerhtml += f"<tr class=''><th><a href='/{''.join(substring.split('/')[:-1])}' class='btn btn-primary'>↑back↑</a></th><th style='padding: 0px; width: 50%;'><span id='currentsong'></span></th></tr>" if subpath else ""
        for i in directory_list:
            if "." not in i:
                innerhtml += f"<tr><th colspan='2'><a href='{'/' + substring if subpath else ''}/{i}' class='btn btn-success'>{i}</a></th></tr>"
            elif ".mp3" in i:
                innerhtml += f"<tr class=''><th>{i.replace('.mp3', '')}</th><td class='d-flex justify-content-start'><audio controls preload='none' src='{'/' + substring if subpath else ''}/{i}'</td></tr>"
        innerhtml += "</table>"

        title = "index"
        if subpath:
            title = substring.split("/")[-1]

        return render_template("index.html", body=innerhtml, title=title)
    else:
        return redirect("/authenticate")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)