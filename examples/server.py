# requires flask
# basic example web server for serving .reg files
# client can access any filename with GET request,
# and the content of the file is generated based on query
# parameters. For example, one might do:
# GET /install.reg?name=Something&text=Click+me&command=cmd.exe+%1&extension=.txt&extension=.nfo

from flask import Flask, request, make_response
from contextext import ContextEntry 

app = Flask(__name__)

@app.route('/<filename>')
def reg(filename):
    entry = ContentEntry()
        .name(request.args["name"])
        .text(request.args["text"])
        .command(request.args["command"])
        .extensions(set(request.args["extension"]))
    if request.args["for"] == "uninstall":
        return make_response(entry.diff(True))
    else:
        return make_response(entry.removal_diff(True))
    
